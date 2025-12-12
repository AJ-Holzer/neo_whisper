# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import yaml  # type: ignore[import-untyped]
import os

from notification_handlers.notification_handlers_interface import (
    raise_exception,
    notify,
)
from typing import Optional, cast


CONFIG_FILE_PATH: str = "config.yml"
DEFAULT_CONFIG: dict[str, str] = {
    "hotkey": "f9",
    "model_size": "large",
    "sample_rate": "16000",
    "channels": "1",
    "language": "en",
}
REQUIRED_CONFIG_KEYS: list[str] = [
    "hotkey",
    "model_size",
    "sample_rate",
    "channels",
    "language",
]


class Config:
    """A class for managing configurations."""

    def __init__(
        self,
        config_file_path: str = CONFIG_FILE_PATH,
        default_config: dict[str, str] = DEFAULT_CONFIG,
        required_config_keys: list[str] = REQUIRED_CONFIG_KEYS,
    ) -> None:
        """Automatically loads and saves the config to the config file.

        Args:
            config_file_path (str, optional): The file path of the config file. Defaults to CONFIG_FILE_PATH.
            default_config (dict[str, str], optional): The default config to use. Defaults to DEFAULT_CONFIG.
            required_config_keys (list[str], optional): The required config keys. Defaults to REQUIRED_CONFIG_KEYS.
        """
        self.__data: dict[str, str] = {}
        self.__config_file_path: str = config_file_path
        self.__default_config: dict[str, str] = default_config
        self.__required_config_keys: list[str] = required_config_keys

        self.__load_config_file()

    def __config_valid(self, config_data: Optional[dict[str, str]]) -> bool:
        """Checks if the config data is valid.

        Args:
            config_data (dict[str, str]): The config from the config file.

        Returns:
            bool: Whether the config is valid or not.
        """
        return (
            config_data is not None
            and config_data.keys() == self.__required_config_keys
        )

    def __get_config(self) -> Optional[dict[str, str]]:
        """Reads the data of the config file.

        Returns:
            dict[str, str]: The data of the config file.
        """
        if not os.path.exists(self.__config_file_path):
            return None

        with open(file=self.__config_file_path, mode="r", encoding="UTF-8") as f:
            return yaml.safe_load(stream=f)

    def __save_config(self, config: Optional[dict[str, str]] = None) -> None:
        """Saves the provided config to the config file.

        Args:
            config (Optional[dict[str, str]], optional): The config to save. If config is set to None, default config will be used. Defaults to None.
        """
        with open(file=self.__config_file_path, mode="w", encoding="UTF-8") as f:
            yaml.dump(data=config, stream=f)

    def __load_config_file(self) -> None:
        """
        Loads the config file.
        If there is no config provided, the default config will be used and saved to the config file.
        """
        # Load config data
        config: Optional[dict[str, str]] = self.__get_config()

        # Use config file if provided
        if self.__config_valid(config_data=config):
            self.__data = cast(dict[str, str], config)
            return

        # Notify the user about the problem
        notify(msg="No config provided! Using default and creating config file...")

        # Set config to default config
        self.__data = self.__default_config

        # Write config file
        self.__save_config()

    def __getitem__(self, key: str) -> str:
        """Get the value for the specified configuration.

        Args:
            key (str): The key of configuration name.

        Returns:
            str: The Value of the configuration.
        """
        # Check if key exists
        if key not in self.__data:
            raise_exception(msg=f"Key '{key}' does not exist in the config!")

        return self.__data[key]

    def __setitem__(self, key: str, value: str) -> None:
        """Set the value for the specified configuration.

        Args:
            key (str): The configuration name.
            value (str): The value of the configuration.
        """
        # Check if key is allowed
        if key not in self.__required_config_keys:
            raise_exception(
                msg=f"Invalid key '{key}'! Only the following are allowed: {self.__required_config_keys}"
            )

        self.__data[key] = value


config: Config = Config()
