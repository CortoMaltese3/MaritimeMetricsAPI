from flask import Flask, jsonify, request

from config import Config
from .models import MaritimeData

app = Flask(__name__)
app.config.from_object(Config)

csv_path = app.config["CSV_PATH"]
maritime_data = MaritimeData(csv_path)


@app.route("/api/vessel_invalid_data/<int:vessel_code>", methods=["GET"])
def get_vessel_invalid_data(vessel_code):
    invalid_data = maritime_data.get_invalid_data_for_vessel(vessel_code)
    if not invalid_data:
        return (
            jsonify(
                {
                    "message": "No data found for this vessel.",
                    "vessel_code": vessel_code,
                }
            ),
            404,
        )
    return jsonify(
        {
            "message": "Found invalid data for this vessel",
            "vessel_code": vessel_code,
            "invalid_data": invalid_data,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
