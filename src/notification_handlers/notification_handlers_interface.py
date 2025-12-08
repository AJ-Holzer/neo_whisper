# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


def raise_exception(msg: str):
    raise Exception(msg)


def notify(msg: str):
    print(msg)


def log(parent: str, msg: str):
    print(f"{parent} | {msg}")
