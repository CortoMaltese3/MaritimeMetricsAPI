"""
Module containing Flask route definitions for the web application.

This module defines the API endpoints of the web application, handling
the requests to various functionalities such as retrieving invalid data for vessels,
comparing vessel compliance scores, and fetching vessel speed differences. Each route
is associated with a specific function that processes the request and returns a response
to the client.
"""

import json

from flask import Flask, jsonify, Response

from config import Config
from .models import MaritimeData

app = Flask(__name__)
app.config.from_object(Config)

csv_path = app.config["CSV_PATH"]
maritime_data = MaritimeData(csv_path)


@app.route("/api/vessel_invalid_data/<vessel_code>", methods=["GET"])
def get_vessel_invalid_data(vessel_code: str) -> Response:
    """
    Retrieves a summary of invalid data for a specific vessel based on its code.

    :param vessel_code: The unique code identifying the vessel.
    :return: A JSON response containing a summary of invalid data issues.
    :rtype: Response

    Example response:
    ```
    {
        "message": "Found invalid data for this vessel",
        "vessel_code": 3001,
        "invalid_data": {
            "below_zero": {
                "proposed_speed_overground": 30686,
                "predicted_fuel_consumption": 1669,
                "power": 1375
            },
            ...
    ```
    """
    try:
        vessel_code_int = int(vessel_code)
    except ValueError:
        return (
            jsonify(
                {"message": "Invalid vessel code format.", "vessel_code": vessel_code}
            ),
            400,
        )

    invalid_data = maritime_data.get_invalid_data_for_vessel(vessel_code_int)
    if not invalid_data:
        return (
            jsonify(
                {
                    "message": "No data found for this vessel.",
                    "vessel_code": vessel_code_int,
                }
            ),
            404,
        )

    # Added this approach to avoid structure data issues with jsonify messing
    # with the dictionary structure
    return Response(
        json.dumps(
            {
                "message": "Found invalid data for this vessel",
                "vessel_code": vessel_code_int,
                "invalid_data": invalid_data,
            },
        ),
        mimetype="application/json",
    )


@app.route("/api/vessel_speed_difference/<vessel_code>", methods=["GET"])
def get_vessel_speed_difference(vessel_code: str) -> Response:
    """
    Provides the speed differences between actual and proposed speeds for a vessel.

    :param vessel_code: The unique code identifying the vessel.
    :return: A JSON response containing the speed differences for the vessel.
    :rtype: Response

    Example response:
    ```
    {
        "message": "Speed differences for the vessel",
        "vessel_code": 19310,
        "speed_differences": [
            {
                "latitude": 49.2837677001953,
                "longitude": -123.177825927734,
                "speed_difference": 0.747206647694111
            },
            ...
        ]
    }
    ```
    """
    try:
        vessel_code_int = int(vessel_code)
    except ValueError:
        return (
            jsonify(
                {"message": "Invalid vessel code format.", "vessel_code": vessel_code}
            ),
            400,
        )

    speed_differences = maritime_data.get_speed_differences_for_vessel(vessel_code_int)
    if not speed_differences:
        return (
            jsonify(
                {
                    "message": "No data found for this vessel or no speed differences calculated.",
                    "vessel_code": vessel_code_int,
                }
            ),
            404,
        )

    return Response(
        json.dumps(
            {
                "message": "Speed differences for the vessel",
                "vessel_code": vessel_code_int,
                "speed_differences": speed_differences,
            }
        ),
        mimetype="application/json",
    )


@app.route(
    "/api/vessel_compliance_comparison/<vessel_code1>/<vessel_code2>", methods=["GET"]
)
def vessel_compliance_comparison(vessel_code1: str, vessel_code2: str) -> Response:
    """
    Compares the compliance scores between two vessels based on their speed adherence.

    :param vessel_code1: The unique code identifying the first vessel.
    :param vessel_code2: The unique code identifying the second vessel.
    :return: A JSON response indicating the comparison result.
    :rtype: Response

    Example response:
    ```
    {
        "message": "Vessel 19310 is more compliant with a compliance score of 83.54%
                    compared to Vessel 3001's score of 72.11%."
    }
    ```
    """
    try:
        vessel_code1_int = int(vessel_code1)
        vessel_code2_int = int(vessel_code2)
    except ValueError:
        return jsonify({"message": "Invalid vessel code format."}), 400

    comparison_result = maritime_data.compare_vessel_compliance(
        vessel_code1_int, vessel_code2_int
    )

    # Check if the result is an error message indicating a non-existent vessel code
    if "does not exist" in comparison_result:
        return jsonify({"message": comparison_result}), 404

    return jsonify({"message": comparison_result})


@app.route("/api/vessel_metrics/<vessel_code>/<start_date>/<end_date>", methods=["GET"])
def get_vessel_metrics(vessel_code: str, start_date: str, end_date: str) -> Response:
    """
    Retrieves metrics for a specific vessel within a given time period.

    :param vessel_code: The unique code identifying the vessel.
    :param start_date: The start date of the period (inclusive).
    :param end_date: The end date of the period (inclusive).
    :return: A JSON response containing the metrics for the specified vessel and period.
    :rtype: Response

    Example response:
    ```
    [
        {
            "vessel_code": 3001,
            "datetime": "2023-06-01 00:01:00",
            "latitude": 10.2894496918,
            "longitude": -14.7888498306,
            "power": 0.0,
            "fuel_consumption": 0.0,
            "actual_speed_overground": 0.09999,
            "proposed_speed_overground": 0.9464979896,
            "predicted_fuel_consumption": 0.0,
            "speed_difference": 0.8465079896
        },
      ...
    ]
    ```
    """
    try:
        vessel_code_int = int(vessel_code)
    except ValueError:
        return jsonify({"message": "Invalid vessel code format."}), 400

    metrics_data = maritime_data.get_metrics_for_vessel_period(
        vessel_code_int, start_date, end_date
    )

    # Use .empty to check if the DataFrame is empty
    if metrics_data.empty:
        return (
            jsonify(
                {
                    "message": "No data found for this vessel within the specified period."
                }
            ),
            404,
        )

    metrics_json = metrics_data.to_json(orient="records")
    return Response(metrics_json, mimetype="application/json")


@app.route(
    "/api/vessel_raw_metrics/<vessel_code>/<start_date>/<end_date>", methods=["GET"]
)
def get_vessel_raw_metrics(
    vessel_code: str, start_date: str, end_date: str
) -> Response:
    """
    Retrieves raw data metrics for a specific vessel over a specified period.

    :param vessel_code: The unique code identifying the vessel.
    :param start_date: The start date of the period (inclusive).
    :param end_date: The end date of the period (inclusive).
    :return: A JSON response containing the raw data for the vessel within the specified period.
    :rtype: Response

    Example response:
    ```
    [
        {
            "vessel_code": 3001,
            "datetime": "2023-06-01 00:00:00",
            "latitude": 10.2894458771,
            "longitude": -14.7888755798,
            "power": 0.0,
            "fuel_consumption": 0.0,
            "actual_speed_overground": 0.039996,
            "proposed_speed_overground": -0.1899042625,
            "predicted_fuel_consumption": 0.0
        },
      ...
    ]
    ```
    """
    try:
        vessel_code_int = int(vessel_code)
    except ValueError:
        return jsonify({"message": "Invalid vessel code format."}), 400

    raw_data = maritime_data.get_raw_metrics_for_vessel_period(
        vessel_code_int, start_date, end_date
    )

    if raw_data.empty:
        return (
            jsonify(
                {
                    "message": "No raw data found for this vessel within the specified period."
                }
            ),
            404,
        )

    raw_data_json = raw_data.to_json(orient="records")
    return Response(raw_data_json, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
