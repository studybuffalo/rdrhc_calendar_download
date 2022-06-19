"""Downloads the RDRHC schedules for upload to the parsing server.

    Last Update: 2022-Jun-18

    Copyright (c) Notices
        2022	Joshua R. Torrance	<joshua@torrance.io>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not,
    see <http://www.gnu.org/licenses/>.

    SHOULD YOU REQUIRE ANY EXCEPTIONS TO THIS LICENSE, PLEASE CONTACT
    THE COPYRIGHT HOLDERS.
"""
import pathlib
import sys
import time

from . import Config, Log, setup_session, download_schedule, setup_sftp, upload_schedule


def main():
    """Organizes and runs the extraction script."""
    # APPLICATION SETUP
    # ------------------------------------------------------------------------
    # Retrieve path to config file
    config_path = pathlib.Path(sys.argv[1])

    # Setup config deatils
    config = Config(config_path)

    # Setup Logging
    log = Log(config)

    # DOWNLOAD PROCESS
    # ------------------------------------------------------------------------
    log.info('RDRHC CALENDAR DOWNLOAD SCRIPT STARTED.')

    # Setup the requests session
    session = setup_session(config, log)

    # Loop through all roles and download schedule data
    file_contents = {}

    for role, details in config.download.schedule_details.items():
        file_contents[role] = {
            'data': download_schedule(details, session, role, log),
            'name': f'{role}_{int(time.time())}.{details["extension"]}',
        }

    # Close the session
    session.close()

    # Setup the SFTP client
    ssh_client, sftp_client = setup_sftp(config, log)

    # Loop through the file content and upload files
    for _, file in file_contents.items():
        upload_schedule(file, sftp_client, log)

    # Close the SSH and SFTP client
    ssh_client.close()
    sftp_client.close()

    # Return 0 to confirm successful completion
    log.info('RDRHC CALENDAR DOWNLOAD SCRIPT COMPLETE.')

    return 0


if __name__ == '__main__':
    sys.exit(main())
