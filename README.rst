==============================
RDRHC Calendar Download Script
==============================
This script visits a restricted SharePoint page, downloads the
specified schedules, and then uploads to another server via SFTP.

-------------
Running Tests
-------------

To run tests::

  $ pipenv run pytest

To generate coverage report::

  # XML Report
  $ pipenv run pytest --cov test --cov-report xml

  # HTML Report
  $ pipenv run pytest --cov test --cov-report html

---------------
Running Linters
---------------

To run linting::

  # Run Pylint
  $ pipenv run pylint **/**.py

  # Run Pycodestyle
  $ pipenv run pycodestyle **/**.py

-------------------
Documentation Style
-------------------

Docstrings are documented using the reStructuredText format. Details of
this style can be found here:
https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html
