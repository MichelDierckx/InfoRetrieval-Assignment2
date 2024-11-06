from typing import Optional

import configargparse


class Config:
    """
    Command-line and file-based configuration handler. Makes use of the singleton pattern.

    Configuration settings can be specified in a config.ini file (by default in
    the working directory), or as command-line arguments.
    """

    _instance = None  # To ensure only one instance (singleton)

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
            help="Directory that will contain the index.",
        )
        self._parser.add_argument(
            "--analyzer",
            required=True,
            default="standard",
            help="The analyzer to be used (simple, standard, whitespace, stop, stem)",
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


# Instantiate a shared configuration object for global access. Only one can exist.
config = Config()
