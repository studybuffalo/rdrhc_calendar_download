"""Module to download the RDRHC schedules."""
import urllib


def download_schedule(details, session, role, log):
    """Downloads the requested schedule and returns data.

        Args:
            details (dict): contains the schedule download details.
            session (obj): an authenticated requests Session object.
            role (str): the role for the schedule.
            config (obj): a Config object.
            log (obj): a Log object.

        Returns:
            byte: the downloaded schedule data.
    """
    log.info(f'Downloading {role} schedule.')

    # Assemble the download URL
    url = f'{details["directory"]}{urllib.parse.quote(details["name"])}.{details["extension"]}'

    log.debug(f'Requesting file from URL: "{url}".')

    download = session.get(url)

    log.debug(f'Response status code: {download.status_code}')

    if download.status_code != 200:
        raise FileNotFoundError(f'Unable to download file: "{url}".')

    return download.content
