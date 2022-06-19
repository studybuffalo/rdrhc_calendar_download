"""Manages details around script configuration."""
import configparser
from decimal import Decimal
from pathlib import Path
from typing import NamedTuple


class Config:  # pylint: disable=too-few-public-methods
    """Class to hold configuration details."""
    def __init__(self, config_path):
        """Initialization details for Config class.

            Args:
                config_path (str):

            Attributes:
                config_path: a Path object to the script's config file.
                sentry: A named tuple containing Sentry config details.
                api: A named tuple containing API config details.
        """
        self.config_path = Path(config_path)
        self.logging = None
        self.download = None
        self.upload = None

        self._assemble_app_configuration_details()

    class LoggingDetails(NamedTuple):
        """Describes Logging configuration details."""
        enable_sentry: bool
        dsn: str
        environment: str
        sample_rate: Decimal
        sentry_debug: bool
        enable_stdout: bool
        stdout_level: int

    class DownloadDetails(NamedTuple):
        """Describes HC DPD extract download configuration details."""
        driver_path: str
        schedule_home: str
        schedule_details: dict
        schedule_user: str
        schedule_password: str

    class UploadDetails(NamedTuple):
        """Describes HC DPD upload configuration details."""
        host_name: str
        port: int
        user_name: str
        key_path: str
        key_pass: str
        host_key: str
        upload_directory: str

    def _assemble_app_configuration_details(self):
        """Collects and assigns all the relevant configuration details.

            Loads the config file with the provided Path. Once loaded,
            retrieves all config details and parses into correct
            formats and types.

            Updates object attributes with these details.
        """
        # Read the config file from the provided root
        config = configparser.ConfigParser(
            converters={'decimal': Decimal}
        )
        config.read(self.config_path)

        # Raise alert if no config file found
        if not config.sections():
            raise FileNotFoundError('Config file not found or is empty.')

        # Call methods to assign various details
        self._assign_logging_details(config)
        self._assign_download_details(config)
        self._assign_upload_details(config)

    def _assign_logging_details(self, config):
        """Assigns details for tracking & logging.

            Args:
                config (obj): a ConfigParser object containing
                    configuration details for script.
        """
        self.logging = self.LoggingDetails(
            config.getboolean('logging', 'enable_sentry', fallback=False),
            config.get('logging', 'dsn', fallback='https://A@sentry.io/1'),
            config.get('logging', 'environment', fallback='production'),
            config.getdecimal('logging', 'sample_rate', fallback='1.0'),
            config.getboolean('logging', 'sentry_debug', fallback=False),
            config.getboolean('logging', 'enable_stdout', fallback=True),
            config.getint('logging', 'stdout_level', fallback=10),
        )

    def _assign_download_details(self, config):
        """Assigns details for download & extraction of DPD data.

            Args:
                config (obj): a ConfigParser object containing
                    configuration details for script.
        """
        self.download = self.DownloadDetails(
            config.get('download', 'driver_path'),
            config.get('download', 'schedule_home'),
            {
                'assistant': {
                    'directory': config.get('download', 'schedule_directory_a'),
                    'name': config.get('download', 'schedule_name_a'),
                    'extension': config.get('download', 'schedule_ext_a'),
                },
                'pharmacist': {
                    'directory': config.get('download', 'schedule_directory_p'),
                    'name': config.get('download', 'schedule_name_p'),
                    'extension': config.get('download', 'schedule_ext_p'),
                },
                'technician': {
                    'directory': config.get('download', 'schedule_directory_t'),
                    'name': config.get('download', 'schedule_name_t'),
                    'extension': config.get('download', 'schedule_ext_t'),
                },
            },
            config.get('download', 'schedule_user'),
            config.get('download', 'schedule_password'),
        )

    def _assign_upload_details(self, config):
        """Assigns details for API upload.

            Args:
                config (obj): a ConfigParser object containing
                    configuration details for script.
        """
        self.upload = self.UploadDetails(
            config.get('upload', 'host_name'),
            config.getint('upload', 'port', fallback=22),
            config.get('upload', 'user_name'),
            config.get('upload', 'key_path'),
            config.get('upload', 'key_pass'),
            config.get('upload', 'host_key'),
            config.get('upload', 'upload_directory'),
        )
