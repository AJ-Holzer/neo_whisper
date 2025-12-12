# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from enum import StrEnum


class ModelDevice(StrEnum):
    CUDA = "cuda"
    CPU = "cpu"
