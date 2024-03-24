"""This module is used to import the data from the CSV file to the database."""

import pandas as pd
from .models import VesselData
from .database import db
from flask import current_app


def import_csv_to_db(csv_path):
    """Import CSV data into the database."""
    df = pd.read_csv(csv_path)

    with current_app.app_context():
        for _, row in df.iterrows():
            vessel_data = VesselData(
                vessel_code=row["vessel_code"],
                datetime=row["datetime"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                power=row["power"],
                fuel_consumption=row["fuel_consumption"],
                actual_speed_overground=row["actual_speed_overground"],
                proposed_speed_overground=row["proposed_speed_overground"],
                predicted_fuel_consumption=row["predicted_fuel_consumption"],
            )
            db.session.add(vessel_data)
        db.session.commit()
