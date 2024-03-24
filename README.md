# MaritimeMetrics API

## Overview

The Marine Metrics API is a Python-based application for analyzing maritime data, including vessel compliance, speed differences, and metrics over specific time periods. It provides a set of functionalities to filter and analyze maritime data to improve decision-making processes in maritime operations.

## Features

- **Vessel Data Retrieval**: Fetch raw and filtered data for vessels.
- **Compliance Score Calculation**: Compare compliance scores based on speed adherence between vessels.
- **Speed Difference Calculation**: Calculate the speed differences between actual and proposed speeds for vessels.
- **Data Filtering**: Filter invalid data, including outliers, missing values, and incorrect geocoordinates.
- **Reporting**: Report invalid data and produce suggestions.

## Dependencies

The application requires reading data from a CSV file. The path to this CSV file is configurable via the `CSV_PATH` parameter in the `config.py` file. The default dataset is the `data/vessel_data.csv`

## Setup and Running the Application

### For Developers

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/CortoMaltese3/MaritimeMetricsAPI.git
   cd MaritimeMetricsAPI
   git checkout main
   ```
2. **Set Up a Virtual Environment** (optional but recommended):

   ```sh
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   # Or using Conda
   conda create --name maritime python=3.8
   conda activate maritime
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Create a `.env` File** based on the `.env.template` in the root directory.
5. **Start the Flask Application Locally**:
   ```sh
   flask run
   ```

### For Production

1. **Ensure Docker and Docker-Compose are Installed**:
   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)
2. Follow steps 1 to 4 from the Developers section.
3. **Use Docker Compose to Run the Application**:
   ```sh
   docker-compose up --build
   ```

## API Endpoints

- **Get Vessel Invalid Data**:
  `GET /api/vessel_invalid_data/<vessel_code>`
- **Get Vessel Speed Difference**:
  `GET /api/vessel_speed_difference/<vessel_code>`
- **Compare Vessel Compliance**:
  `GET /api/vessel_compliance_comparison/<vessel_code1>/<vessel_code2>`
- **Get Vessel Metrics**:
  `GET /api/vessel_metrics/<vessel_code>/<start_date>/<end_date>`
- **Get Raw Vessel Metrics**:
  `GET /api/vessel_raw_metrics/<vessel_code>/<start_date>/<end_date>`

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of requests:

- `200 OK`: The request was successful.
- `400 Bad Request`: The request was invalid or cannot be served.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: An error occurred in the server.

## Logging

The application logs important actions and errors, facilitating debugging and monitoring. The logs are stored locally in the app.log file.

## Documentation

Developer documentation, including a detailed description of API endpoints and usage examples, can be found [here](https://cortomaltese3.github.io/MaritimeMetricsAPI/).

## Before Opening a Pull Request

Ensure you run the tests and comply with the linting standards before opening a pull request:

- Run tests: `python -m unittest tests/test_api.py`
- Check linting: `pylint app/ --fail-under=8`
  Failure to meet the test coverage and linting standards will result in CI pipeline failures.


## API Testing with Swagger UI
MarineMetricsAPI includes a Swagger UI interface that allows developers and users to interactively test the API endpoints without writing any code. The Swagger UI provides a web-based interface where you can see all available API endpoints, their required parameters, and even execute API calls directly from your browser. More information can be found in the [documentation](https://cortomaltese3.github.io/MaritimeMetricsAPI/setup.html).

