# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


class Notifier:
    @staticmethod
    def exception(msg: str):
        raise Exception(msg)

    @staticmethod
    def notify(msg: str):
        print(msg)
