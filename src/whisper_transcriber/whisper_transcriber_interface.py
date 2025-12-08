# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import whisper
import sounddevice as sd
import numpy as np
import time
import torch

from notifier.notifier_interface import Notifier


class WhisperTranscriber:
    def __init__(self) -> None: ...

    def transcribe(self) -> None: ...
