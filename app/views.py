"""
Module containing Flask route definitions for the web application.

This module defines the API endpoints of the web application, handling
the requests to various functionalities such as retrieving invalid data for vessels,
comparing vessel compliance scores, and fetching vessel speed differences. Each route
is associated with a specific function that processes the request and returns a response
to the client.
"""

from datetime import datetime
import json
import logging

from flask import jsonify, Response, request
from flasgger import swag_from

from .data_analysis import DataAnalyzer
from . import app

maritime_data = app.config["maritime_data"]


@app.route("/api/vessel_invalid_data/<vessel_code>", methods=["GET"])
@swag_from("docs/vessel_invalid_data.yml")
def get_vessel_invalid_data(vessel_code: str) -> Response:
    """
    Retrieves a summary of invalid data for a specific vessel based on its code.

    :param vessel_code: The unique code identifying the vessel.
    :return: A JSON response containing a summary of invalid data issues.
    :rtype: Response

    Example response::

            {
                "message": "Found invalid data for this vessel",
                "vessel_code": 3001,
                "invalid_data": {
                    "below_zero": {
                        "proposed_speed_overground": 30686,
                        "predicted_fuel_consumption": 1669,
                        "power": 1375
                    }
                    ...
                }
            }
    """
    try:
        if not vessel_code:
            logging.warning("Vessel code cannot be empty.")
            return jsonify({"message": "Vessel code cannot be empty."}), 400
        vessel_code_int = int(vessel_code)
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

        return Response(
            json.dumps(
                {
                    "message": "Found invalid data for this vessel",
                    "vessel_code": vessel_code_int,
                    "invalid_data": invalid_data,
                }
            ),
            mimetype="application/json",
        )
    except ValueError:
        logging.warning(f"Invalid vessel code format received: {vessel_code}")
        return (
            jsonify(
                {"message": "Invalid vessel code format.", "vessel_code": vessel_code}
            ),
            400,
        )
    except Exception as e:
        logging.error(f"Error retrieving invalid data for vessel {vessel_code}: {e}")
        return jsonify({"message": "An error occurred processing your request."}), 500


@app.route("/api/vessel_speed_difference/<vessel_code>", methods=["GET"])
@swag_from("docs/vessel_speed_difference.yml")
def get_vessel_speed_difference(vessel_code: str) -> Response:
    """
    Provides the speed differences between actual and proposed speeds for a vessel.

    :param vessel_code: The unique code identifying the vessel.
    :return: A JSON response containing the speed differences for the vessel.
    :rtype: Response

    Example response::

            {
                "message": "Speed differences for the vessel",
                "vessel_code": 19310,
                "speed_differences": [
                    {
                        "latitude": 49.2837677001953,
                        "longitude": -123.177825927734,
                        "speed_difference": 0.747206647694111
                    }
                    ...
                ]
            }
    """
    try:
        if not vessel_code:
            logging.warning("Vessel code cannot be empty.")
            return jsonify({"message": "Vessel code cannot be empty."}), 400
        vessel_code_int = int(vessel_code)
        speed_differences = maritime_data.get_speed_differences_for_vessel(
            vessel_code_int
        )
        if not speed_differences:
            return (
                jsonify(
                    {
                        "message": "No data found for this vessel or no speed differences.",
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
    except ValueError:
        logging.warning(f"Invalid vessel code format received: {vessel_code}")
        return (
            jsonify(
                {"message": "Invalid vessel code format.", "vessel_code": vessel_code}
            ),
            400,
        )
    except Exception as e:
        logging.error(
            f"Error retrieving speed differences for vessel {vessel_code}: {e}"
        )
        return jsonify({"message": "An error occurred processing your request."}), 500


@app.route(
    "/api/vessel_compliance_comparison/<vessel_code1>/<vessel_code2>", methods=["GET"]
)
@swag_from("docs/vessel_compliance_comparison.yml")
def vessel_compliance_comparison(vessel_code1: str, vessel_code2: str) -> Response:
    """
    Compares the compliance scores between two vessels based on their speed adherence.

    :param vessel_code1: The unique code identifying the first vessel.
    :param vessel_code2: The unique code identifying the second vessel.
    :return: A JSON response indicating the comparison result.
    :rtype: Response

    Example response::

            {
                "message": "Vessel 19310 is more compliant with a compliance score of 83.54%
                            compared to Vessel 3001's score of 72.11%."
            }
    """
    try:
        if not vessel_code1 or not vessel_code2:
            logging.warning("Vessel code cannot be empty.")
            return jsonify({"message": "Vessel code cannot be empty."}), 400
        vessel_code1_int, vessel_code2_int = map(int, [vessel_code1, vessel_code2])
        comparison_result = maritime_data.compare_vessel_compliance(
            vessel_code1_int, vessel_code2_int
        )

        # Check if the comparison_result indicates a non-existent vessel code
        if "does not exist" in comparison_result:
            # This checks if the comparison_result contains a message about non-existence
            logging.info(
                f"One or both vessel codes do not exist: {vessel_code1}, {vessel_code2}"
            )
            return jsonify({"message": comparison_result}), 404

        return jsonify({"message": comparison_result})
    except ValueError:
        logging.warning(
            f"Invalid vessel code format received: {vessel_code1} or {vessel_code2}"
        )
        return jsonify({"message": "Invalid vessel code format."}), 400
    except Exception as e:
        logging.error(
            f"Error comparing compliance for vessels {vessel_code1} and {vessel_code2}: {e}"
        )
        return jsonify({"message": "An error occurred processing your request."}), 500


@app.route("/api/vessel_metrics/<vessel_code>/<start_date>/<end_date>", methods=["GET"])
@swag_from("docs/vessel_metrics.yml")
def get_vessel_metrics(vessel_code: str, start_date: str, end_date: str) -> Response:
    """
    Retrieves metrics for a specific vessel within a given time period.

    :param vessel_code: The unique code identifying the vessel.
    :param start_date: The start date of the period (inclusive).
    :param end_date: The end date of the period (inclusive).
    :return: A JSON response containing the metrics for the specified vessel and period.
    :rtype: Response

    Example response::

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
                }
                ...
            ]
    """
    try:
        if not vessel_code:
            logging.warning("Vessel code cannot be empty.")
            return jsonify({"message": "Vessel code cannot be empty."}), 400
        vessel_code_int = int(vessel_code)
        if not all(
            map(lambda x: datetime.strptime(x, "%Y-%m-%d"), [start_date, end_date])
        ):
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        metrics_data = maritime_data.get_metrics_for_vessel_period(
            vessel_code_int, start_date, end_date
        )
        if metrics_data.empty:
            return (
                jsonify(
                    {
                        "message": "No data found for this vessel within the specified period."
                    }
                ),
                404,
            )
        return Response(
            metrics_data.to_json(orient="records"), mimetype="application/json"
        )
    except ValueError as e:
        logging.warning(f"Invalid input received: {e}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logging.error(
            f"Error retrieving metrics for {vessel_code} between {start_date} and {end_date}: {e}"
        )
        return jsonify({"message": "An error occurred processing your request."}), 500


@app.route(
    "/api/vessel_raw_metrics/<vessel_code>/<start_date>/<end_date>", methods=["GET"]
)
@swag_from("docs/vessel_raw_metrics.yml")
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

    Example response::


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
                }
                ...
            ]
    """
    try:
        if not vessel_code:
            logging.warning("Vessel code cannot be empty.")
            return jsonify({"message": "Vessel code cannot be empty."}), 400
        vessel_code_int = int(vessel_code)
        # Date validation as performed in get_vessel_metrics
        if not all(
            map(lambda x: datetime.strptime(x, "%Y-%m-%d"), [start_date, end_date])
        ):
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
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
        return Response(raw_data.to_json(orient="records"), mimetype="application/json")
    except ValueError as e:
        logging.warning(f"Invalid input received: {e}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logging.error(
            f"Error retrieving metrics for {vessel_code} between {start_date} and {end_date}: {e}"
        )
        return jsonify({"message": "An error occurred processing your request."}), 500


@app.route("/api/vessel_problems/<vessel_code>", methods=["GET"])
# @swag_from("docs/vessel_problems.yml")  # Make sure to create this YAML file
def get_vessel_problems(vessel_code: str):
    """
    Retrieves a summary of problematic data groups for a specific vessel.

    :param vessel_code: The unique code identifying the vessel.
    :return: A JSON response containing the summary of problematic data groups.
    :rtype: Response
    """
    problem_type = request.args.get("problem_type", default="missing_values")
    column_name = request.args.get(
        "column_name", None
    )  # Get column_name from query parameters

    if not column_name:
        logging.warning("Column name must be specified.")
        return jsonify({"message": "Column name must be specified."}), 400

    try:
        vessel_code_int = int(vessel_code)
        data_analyzer = DataAnalyzer()
        data_analyzer.filter_by_vessel(
            vessel_code_int
        )  # Filter the data for the specified vessel

        # Get a summary of problematic data based on the specified problem_type and column_name
        summary = data_analyzer.get_problematic_data_summary(column_name, problem_type)
        return jsonify(summary), 200
    except ValueError as e:
        logging.warning(f"Invalid input received: {e}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logging.error(f"Error retrieving problem summary for vessel {vessel_code}: {e}")
        return jsonify({"message": "An error occurred processing your request."}), 500


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
