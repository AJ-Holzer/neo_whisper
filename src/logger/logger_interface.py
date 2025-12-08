# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


class Logger:
    @staticmethod
    def exception(msg: str):
        raise Exception(msg)

    @staticmethod
    def notify(msg: str):
        print(msg)

    @staticmethod
    def log(parent: str, msg: str):
        print(f"{parent} | {msg}")
