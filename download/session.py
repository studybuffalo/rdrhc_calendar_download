"""Module to download the RDRHC schedules."""
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def setup_session(config, log):
    """Downloads the requested schedule and returns data.

        Args:
            config (obj): a Config object.
            log (obj): a Log object.

        Returns:
            obj: a requests Session object.
    """
    log.info('Setting up authenticated session.')

    # Setup Selenium webdriver
    with webdriver.Firefox(service=Service(config.download.driver_path)) as driver:
        # Make initial call and get the login page
        log.debug('Calling login page via Selenium webdriver.')
        driver.get(config.download.schedule_home)

        # Retrieve each element (wait 5 seconds for timeout)
        log.debug('Retrieving references to login form via Selenium webdriver.')
        user_name_field = WebDriverWait(driver, 15).until(
            expected_conditions.presence_of_element_located((By.ID, 'userNameInputDisplay'))
        )
        password_field = WebDriverWait(driver, 15).until(
            expected_conditions.presence_of_element_located((By.ID, 'passwordInput'))
        )
        submit_button = WebDriverWait(driver, 15).until(
            expected_conditions.presence_of_element_located((By.ID, 'submitButton'))
        )

        # Fill out fields and submit form
        log.debug('Filling out login form via Selenium webdriver.')
        user_name_field.send_keys(config.download.schedule_user)
        password_field.send_keys(config.download.schedule_password)
        submit_button.click()

        # Wait for the home page to load to allow cookies to be set
        log.debug('Waiting for home page to load.')
        WebDriverWait(driver, 15).until(
            expected_conditions.url_to_be(config.download.schedule_home)
        )

        # Copy cookies from Selenium to a requests session
        log.debug('Copying cookies from Selenium to requests session.')
        session = requests.Session()
        selenium_cookies = driver.get_cookies()

        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])

    return session
