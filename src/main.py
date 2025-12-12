# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import time

from whisper_stt.whisper_stt_interface import WhisperTranscriber


def main() -> None:
    whisper_transcriber: WhisperTranscriber = WhisperTranscriber(audio_device_id=7)

    whisper_transcriber.start_recording()
    time.sleep(5)
    text: str | None = whisper_transcriber.stop_recording()

    print(text)


if __name__ == "__main__":
    main()
