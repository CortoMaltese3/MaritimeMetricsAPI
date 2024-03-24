.. MarineMetricsAPI documentation master file, created by
   sphinx-quickstart on Sat Mar 23 19:09:41 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the MarineMetricsAPI's documentation!
=================================================

Overview
--------
The Marine Metrics API is a Python-based application for analyzing maritime data, including vessel compliance, speed differences, and metrics over specific time periods. It provides a set of functionalities to filter and analyze maritime data to improve decision-making processes in maritime operations.

Dependencies
------------
The application requires reading data from a CSV file. The path to this CSV file is configurable via the `CSV_PATH` parameter in the `config.py` file. The default dataset is the `data/vessel_data.csv`.

Setup and Running the Application
---------------------------------
.. include:: ./setup.rst

Logging
-------
The application logs important actions and errors, facilitating debugging and monitoring. The logs are stored locally in the `app.log` file.

Documentation
-------------
Developer documentation, including a detailed description of API endpoints and usage examples, can be found `here <https://cortomaltese3.github.io/MaritimeMetricsAPI/>`_.

Before Opening a Pull Request
------------------------------
Ensure you run the tests and comply with the linting standards before opening a pull request.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
