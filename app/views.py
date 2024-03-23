from flask import Flask, jsonify, request, Response
import json

from config import Config
from .models import MaritimeData

app = Flask(__name__)
app.config.from_object(Config)

csv_path = app.config["CSV_PATH"]
maritime_data = MaritimeData(csv_path)


@app.route("/api/vessel_invalid_data/<vessel_code>", methods=["GET"])
def get_vessel_invalid_data(vessel_code):
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
def get_vessel_speed_difference(vessel_code):
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
def vessel_compliance_comparison(vessel_code1, vessel_code2):
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
def get_vessel_metrics(vessel_code, start_date, end_date):
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
def get_vessel_raw_metrics(vessel_code, start_date, end_date):
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
    app.run(debug=True)
