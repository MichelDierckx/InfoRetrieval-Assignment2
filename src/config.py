import os
from typing import Optional

import configargparse


class Config:
    """
    Command-line and file-based configuration handler. Makes use of the singleton pattern.

    Configuration settings can be specified in a config.ini file (by default in
    the working directory), or as command-line arguments.
    """

    _instance = None  # To ensure only one instance (singleton)
    VALID_ANALYZERS = ["simple", "standard", "whitespace", "stop", "english", "english_spacy"]
    VALID_SIMILARITIES = ["bm25", "classic"]

    def __new__(cls) -> "Config":
        """
        Ensure only one instance of Config exists (singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the configuration parser and provide default values.
        """
        if self.__dict__.get("_initialized", False):
            return  # An instance already exists, so return

        self._parser = configargparse.ArgParser(
            description="IR: assignment 2",
            default_config_files=["config.ini"],
            args_for_setting_config_path=["-c", "--config"],
            formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
        )
        self._define_arguments()  # Add argument definitions
        self._namespace = None
        self._initialized = True  # set a flag to mark singleton as initialized

    def _define_arguments(self) -> None:
        """
        Define the command-line and config file arguments.
        """
        # arguments
        self._parser.add_argument(
            "--data_dir",
            required=True,
            default="data/documents/full_docs_small",
            help="Directory containing the documents.",
        )
        self._parser.add_argument(
            "--index_dir",
            required=True,
            default="index",
            help="Directory that will contain the indexes.",
        )
        self._parser.add_argument(
            "--analyzer",
            required=True,
            default="standard",
            help="The analyzer to be used (simple, standard, whitespace, stop, english, english_spacy)",
        )
        self._parser.add_argument(
            "--similarity",
            required=True,
            default="bm25",
            help="The similarity model to be used (bm25, classic)",
        )

    def parse(self, args_str: Optional[str] = None) -> None:
        """
        Parse the configuration settings.

        Parameters
        ----------
        args_str : Optional[str]
            If None, arguments are taken from sys.argv; otherwise, a string of arguments.
            Arguments not specified on the command line are taken from the config file.
        """
        self._namespace = vars(self._parser.parse_args(args_str))
        self._validate_analyzer()
        self._validate_data_dir()

    def _validate_analyzer(self) -> None:
        """
        Validate that the specified analyzer is in the list of valid analyzers.
        """
        analyzer = self.get("analyzer")
        if analyzer not in self.VALID_ANALYZERS:
            raise ValueError(f"Invalid analyzer '{analyzer}'. Valid options are: {', '.join(self.VALID_ANALYZERS)}")

    def _validate_data_dir(self) -> None:
        """
        Validate that the specified data directory exists.
        """
        data_dir = self.get("data_dir")
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"Data directory '{data_dir}' does not exist.")

    def _validate_similarity(self) -> None:
        """
        Validate that the specified analyzer is in the list of valid analyzers.
        """
        similarity = self.get("similarity")
        if similarity not in self.VALID_SIMILARITIES:
            raise ValueError(f"Invalid similarity '{similarity}'. Valid options are: {', '.join(self.VALID_ANALYZERS)}")

    def __getattr__(self, option):
        """
        Retrieve configuration options as attributes.

        Raises a KeyError with a helpful message if the option does not exist.
        """
        if self._namespace is None:
            raise RuntimeError("The configuration has not been initialized. Call `parse()` first.")

        if option not in self._namespace:
            raise KeyError(f"The configuration option '{option}' does not exist.")

        return self._namespace[option]

    def __getitem__(self, item):
        return self.__getattr__(item)

    def get(self, option: str, default: Optional[str] = None) -> Optional[str]:
        """
        Retrieve configuration options with a default value if the option does not exist.
        :param option: str, the configuration option to retrieve.
        :param default: Optional[str], the default value to return if the option does not exist. Defaults to None.
        :return: Optional[str], The value of the configuration option or the default value.
        """
        if self._namespace is None:
            raise RuntimeError("The configuration has not been initialized. Call `parse()` first.")
        return self._namespace.get(option, default)


# Instantiate a shared configuration object for global access. Only one can exist.
config = Config()
