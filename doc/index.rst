.. MarineMetricsAPI documentation master file, created by
   sphinx-quickstart on Sat Mar 23 19:09:41 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the MarineMetricsAPI's documentation!
=================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   setup

Overview
--------
The Marine Metrics API is a Python-based application for analyzing maritime data, including vessel compliance, speed differences, and metrics over specific time periods. It provides a set of functionalities to filter and analyze maritime data to improve decision-making processes in maritime operations.

Dependencies
------------
The application requires reading data from a CSV file. The path to this CSV file is configurable via the `CSV_PATH` parameter in the `config.py` file. The default dataset is the `data/vessel_data.csv`.

Logging
-------
The application logs important actions and errors, facilitating debugging and monitoring. The logs are stored locally in the `app.log` file.

Documentation
-------------
Developer documentation, including a detailed description of API endpoints and usage examples, can be found `here <https://cortomaltese3.github.io/MaritimeMetricsAPI/>`_.

Before Opening a Pull Request
------------------------------
Before opening a pull request, please ensure the following steps are completed to maintain code and documentation quality:

1. **Run the Tests**:
   Ensure that all tests pass successfully to maintain application integrity.
   .. code-block:: sh

      python -m unittest tests/test_api.py

2. **Comply with Linting Standards**:
   Your code should comply with established linting standards. The CI pipeline will fail if these standards are not met.
   .. code-block:: sh

      pylint app/ --fail-under=8

3. **Update the Documentation**:
   If your changes affect how users interact with the application or add new features, please update the documentation accordingly. Once updates are made, build the documentation locally to ensure it compiles without errors.
   .. code-block:: sh

      sphinx-build -b html doc/ doc/_build/

   Review the generated HTML files in `doc/_build/` to verify your changes. Include the updated documentation files in your pull request.

4. **Upload Documentation Changes**:
   Along with your code changes, commit any updated documentation files to ensure the documentation remains current and useful for all users.
