# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import whisper  # type: ignore[import-untyped]
import sounddevice as sd  # type: ignore[import-untyped]
import numpy as np
import torch

from notification_handlers.notification_handlers_interface import log, notify
from config import config
from typing import Any, Optional
from whisper_stt.types import ModelDevice


class WhisperTranscriber:
    def __init__(self, audio_device_id: int) -> None:
        self.__audio_device_id: int = audio_device_id

        # Select device where whisper should run
        self.__device: ModelDevice = (
            ModelDevice.CUDA if torch.cuda.is_available() else ModelDevice.CPU
        )
        log(parent=self.__class__.__name__, msg=f"Using device '{self.__device}'")

        # Select model
        self.__model: whisper.Whisper = whisper.load_model(
            name=config["model_size"], device=self.__device
        )
        log(
            parent=self.__class__.__name__,
            msg=f"Loaded model '{config['model_size']}'",
        )

        # Recording variables
        self.__is_recording: bool = False
        self.__audio_data: list[np.ndarray] = []

        # Get device info
        self.__audio_device_info: dict[str, Any] = sd.query_devices(  # type: ignore
            device=self.__audio_device_id
        )
        log(
            parent=self.__class__.__name__,
            msg=f"Selected device: '{self.__audio_device_id}' with name '{self.__audio_device_info['name']}'",
        )

        # Create audio stream
        self.__stream: Optional[sd.InputStream] = None

    def __audio_callback(
        self, indata: np.ndarray, frames: int, time: float, status: sd.CallbackFlags
    ) -> None:
        if status:
            log(parent=self.__class__.__name__, msg=f"Audio status: {status}")
        if self.__is_recording:
            self.__audio_data.append(indata.copy())

    def start_recording(self) -> None:
        """Start recording."""
        # Skip if already recording
        if self.__is_recording:
            return

        # Cleanup and set recording to true
        self.__audio_data = []
        self.__is_recording = True

        log(parent=self.__class__.__name__, msg="Recording...")

        try:
            self.__stream = sd.InputStream(
                samplerate=int(config["sample_rate"]),
                channels=int(config["channels"]),
                callback=self.__audio_callback,
                device=self.__audio_device_id,
                dtype="float32",
            )
            self.__stream.start()
        except Exception as e:
            log(parent=self.__class__.__name__, msg=f"Exception has occurred: {e}")
            self.__is_recording = False

    def stop_recording(self) -> Optional[str]:
        """Stop recording."""
        # Skip if not recording
        if not self.__is_recording:
            return None

        # Set recording to false
        self.__is_recording = False

        # Stop recording
        try:
            if self.__stream is not None:
                self.__stream.stop()
                self.__stream.close()
        except Exception as e:
            log(
                parent=self.__class__.__name__,
                msg=f"There was an error while stopping the stream: {e}",
            )

        # Transcribe audio
        if len(self.__audio_data) > 0:
            return self.__transcribe_audio()
        else:
            log(parent=self.__class__.__name__, msg="No audio recorded.")
            return None

    def __transcribe_audio(self) -> Optional[str]:
        try:
            # Combine audio chunks
            audio_array: np.ndarray = np.concatenate(self.__audio_data, axis=0)
            flattened_audio_array: np.ndarray = audio_array.flatten()

            # Check if audio has sufficient amplitude
            max_amplitude: float = np.abs(flattened_audio_array).max()
            log(
                parent=self.__class__.__name__,
                msg=f"Audio amplitude: {max_amplitude:4f}",
            )

            # Check if audio amplitude is valid
            if max_amplitude < 0.001:
                notify(msg="Audio too quiet - check your microphone!")
                return None

            # Normalize audio
            audio_normalized: np.ndarray = audio_array / max_amplitude

            # Convert audio to float32 for whisper --> whisper prefers float32 between -1 and 1
            audio_float32: np.ndarray = audio_normalized.astype(np.float32)

            # Log debug information
            log(
                parent=self.__class__.__name__,
                msg=f"Audio duration: {len(audio_float32) / float(config['sample_rate']):.2f} seconds",
            )
            log(
                parent=self.__class__.__name__,
                msg=f"Audio shape: {audio_float32.shape}",
            )
            log(
                parent=self.__class__.__name__,
                msg=f"Audio range: [{audio_float32.min():.3f}, {audio_float32.max():.3f}]",
            )

            # Transcribe audio
            result: dict[str, Any] = self.__model.transcribe(  # type: ignore
                audio=audio_float32,
                language=config["language"],
                fp16=self.__device == ModelDevice.CUDA,
                verbose=True,
                temperature=0.0,
                compression_ratio_threshold=2.0,
                logprob_threshold=-0.5,
                no_speech_threshold=0.4,
                condition_on_previous_text=False,
                initial_prompt="",
            )

            # Get detected language
            detected_lang = result.get("language", "unknown")
            log(
                parent=self.__class__.__name__,
                msg=f"Detected language: '{detected_lang}'",
            )

            text: Optional[str] = result.get("text")

            return text if text else None
        except Exception as e:
            print(f"Exception has occurred while transcribing: {e}")

            import traceback

            traceback.print_exc()

            return None
