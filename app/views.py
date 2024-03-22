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


if __name__ == "__main__":
    app.run(debug=True)
