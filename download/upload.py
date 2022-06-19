"""Module to upload the schedule content to the SFTP server."""
import io

import paramiko


def setup_sftp(config, log):
    """Sets up a SFTP client for file upload.

        Args:
            config (obj): a Config object.
            log (obj): a Log object.

        Returns:
            tuple: the SSH client and SFTP client objects.
    """
    log.info('Setting up SFTP client.')

    # Create a SSH Client
    log.debug('Setting up SSH connection with remote server.')

    ssh_client = paramiko.SSHClient()
    ssh_client.load_host_keys(config.upload.host_key)
    ssh_client.connect(
        config.upload.host_name,
        port=config.upload.port,
        username=config.upload.user_name,
        key_filename=config.upload.key_path,
        passphrase=config.upload.key_pass,
    )

    # Open a sftp connection
    log.debug('Setting up SFTP client with remote server.')
    sftp_client = ssh_client.open_sftp()

    log.debug('Moving to proper upload directory.')
    sftp_client.chdir(config.upload.upload_directory)

    return ssh_client, sftp_client


def upload_schedule(file, sftp_client, log):
    """Uploads the provided schedule to SFTP server.
        Args:
            file (dict): the file details to uploads.
            sftp_client (obj): a Paramiko SFTPClient object.
            log (obj): a Log object.
    """
    log.info(f'Uploading schedule data to SFTP server: "{file["name"]}".')

    sftp_client.putfo(io.BytesIO(file['data']), file['name'])
