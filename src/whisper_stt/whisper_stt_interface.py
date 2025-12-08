# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import whisper
import sounddevice as sd
import numpy as np
import time
import torch

from logger.logger_interface import Logger
from config import config


class WhisperTranscriber:
    def __init__(self) -> None:
        # Select device where whisper should run
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        Logger.log(
            parent=self.__class__.__name__, msg=f"Using device '{self.__device}'"
        )

        # Select model
        self.__model: whisper.Whisper = whisper.load_model(
            name=config["model_size"], device=self.__device
        )
        Logger.log(
            parent=self.__class__.__name__,
            msg=f"Loaded model '{config['model_size']}'",
        )

        # Recording variables
        self.__is_recording: bool = False
        self.__audio_data: list[bytes] = []

    def transcribe(self) -> None: ...
