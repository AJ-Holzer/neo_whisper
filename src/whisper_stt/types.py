# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from enum import Enum, auto


class ModelDevice(Enum):
    CUDA = auto()
    CPU = auto()
