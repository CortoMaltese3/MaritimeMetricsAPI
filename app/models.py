import numpy as np
import pandas as pd
from scipy import stats


class MaritimeData:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.raw_data = self._load_csv()
        self.filtered_data = self.raw_data.copy()
        self.invalid_data = {}
        print(f"Original dataset size: {len(self.raw_data)}")
        if not self.raw_data.empty:
            self._filter_invalid_data()
            print(f"Filtered dataset size: {len(self.filtered_data)}")

    def _load_csv(self):
        try:
            return pd.read_csv(self.csv_path)
        except FileNotFoundError:
            print("CSV file not found.")
            return pd.DataFrame()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return pd.DataFrame()

    def _filter_invalid_data(self):
        self._filter_below_zero()
        self._filter_missing_values()
        self._filter_outliers()
        self._filter_invalid_geocoordinates()

    def _filter_below_zero(self):
        condition = lambda col: col < 0
        columns = [
            "power",
            "fuel_consumption",
            "actual_speed_overground",
            "proposed_speed_overground",
            "predicted_fuel_consumption",
        ]
        self._filter_by_condition(condition, "below_zero", columns=columns)

    def _filter_missing_values(self):
        condition = lambda col: col.isna()
        columns = [
            "vessel_code",
            "datetime",
            "latitude",
            "longitude",
            "power",
            "fuel_consumption",
            "actual_speed_overground",
            "proposed_speed_overground",
            "predicted_fuel_consumption",
        ]
        self._filter_by_condition(condition, "missing_value", columns=columns)

    def _filter_outliers(self):
        columns = [
            "power",
            "fuel_consumption",
            "actual_speed_overground",
            "proposed_speed_overground",
            "predicted_fuel_consumption",
        ]
        for column in columns:
            if (
                column in self.filtered_data.columns
                and self.filtered_data[column].dtype != "object"
            ):
                z_scores = stats.zscore(self.filtered_data[column].dropna())
                outlier_mask = (
                    abs(z_scores) > 2
                )  # This can be adjusted depending on how strict we want to be. Leave it as 2 for now.

                full_mask = pd.Series(False, index=self.filtered_data.index)
                non_na_indices = self.filtered_data[column].dropna().index
                full_mask.loc[non_na_indices] = outlier_mask.values  # Ensure alignment

                self._filter_by_condition(lambda col: full_mask, "outlier", [column])

    def _filter_invalid_geocoordinates(self):
        latitude_condition = lambda col: (col < -90) | (col > 90)
        longitude_condition = lambda col: (col < -180) | (col > 180)

        self._filter_by_condition(latitude_condition, "invalid_latitude", ["latitude"])
        self._filter_by_condition(
            longitude_condition, "invalid_longitude", ["longitude"]
        )

    def _filter_by_condition(self, condition_func, problem_type, columns):
        for column in columns:
            mask = condition_func(self.filtered_data[column])
            valid_rows = self.filtered_data.loc[~mask]
            filtered_rows = self.filtered_data.loc[mask]

            # Update the main data with rows where the condition is not met.
            # Add this approach to filter out the invalid rows instead of marking them as invalid
            self.filtered_data = valid_rows

            if not filtered_rows.empty:
                summary = filtered_rows.groupby("vessel_code").size().to_dict()
                for vessel_code, count in summary.items():
                    self.invalid_data.setdefault(vessel_code, {}).setdefault(
                        problem_type, {}
                    ).setdefault(column, 0)
                    self.invalid_data[vessel_code][problem_type][column] += count

    def get_invalid_data_for_vessel(self, vessel_code):
        if vessel_code in self.invalid_data:
            vessel_summary = self.invalid_data[vessel_code]
            sorted_summary = {}
            for problem_type, columns in vessel_summary.items():
                sorted_columns = sorted(
                    columns.items(), key=lambda x: x[1], reverse=True
                )
                sorted_summary[problem_type] = dict(sorted_columns)
            return sorted_summary

    def get_speed_differences_for_vessel(self, vessel_code):
        vessel_data = self.filtered_data[
            self.filtered_data["vessel_code"] == vessel_code
        ].copy()
        if vessel_data.empty:
            return {}

        vessel_data["speed_difference"] = abs(
            vessel_data["actual_speed_overground"]
            - vessel_data["proposed_speed_overground"]
        )

        speed_differences = vessel_data[["latitude", "longitude", "speed_difference"]]
        return speed_differences.to_dict(orient="records")

    def calculate_compliance_score(self, vessel_code):
        vessel_data = self.filtered_data[
            self.filtered_data["vessel_code"] == vessel_code
        ].copy()

        # Avoid division by zero by filtering out proposed speeds that are exactly zero
        vessel_data = vessel_data[vessel_data["proposed_speed_overground"] != 0]

        if len(vessel_data) == 0:
            return 0.0  # Return 0 compliance if there's no data to calculate on

        # Calculate the percentage difference between actual and proposed speeds
        vessel_data["percentage_difference"] = (
            abs(
                vessel_data["actual_speed_overground"]
                - vessel_data["proposed_speed_overground"]
            )
            / vessel_data["proposed_speed_overground"]
        ) * 100

        # Calculate the average of these percentage differences and subtract from 100
        compliance_score = 100 - vessel_data["percentage_difference"].mean()

        # Return the score formatted to two decimal places
        return round(compliance_score, 2)

    def compare_vessel_compliance(self, vessel_code1, vessel_code2):
        # Check if the vessel codes exist in the dataset
        if vessel_code1 not in self.filtered_data["vessel_code"].values:
            return f"Vessel code {vessel_code1} does not exist."

        if vessel_code2 not in self.filtered_data["vessel_code"].values:
            return f"Vessel code {vessel_code2} does not exist."

        score1 = self.calculate_compliance_score(vessel_code1)
        score2 = self.calculate_compliance_score(vessel_code2)

        if score1 > score2:
            return f"Vessel {vessel_code1} is more compliant with a compliance score of {score1}% compared to Vessel {vessel_code2}'s score of {score2}%."
        elif score2 > score1:
            return f"Vessel {vessel_code2} is more compliant with a compliance score of {score2}% compared to Vessel {vessel_code1}'s score of {score1}%."
        else:
            return f"Both vessels have the same compliance score of {score1}%."

    def get_metrics_for_vessel_period(self, vessel_code, start_date, end_date):
        filtered_data = self.filtered_data[
            (self.filtered_data["vessel_code"] == vessel_code)
            & (self.filtered_data["datetime"] >= start_date)
            & (self.filtered_data["datetime"] <= end_date)
        ].copy()

        if filtered_data.empty:
            return {}

        filtered_data["speed_difference"] = abs(
            filtered_data["actual_speed_overground"]
            - filtered_data["proposed_speed_overground"]
        )
        return filtered_data

    def get_raw_metrics_for_vessel_period(self, vessel_code, start_date, end_date):
        raw_data_filtered = self.raw_data[
            (self.raw_data["vessel_code"] == vessel_code)
            & (self.raw_data["datetime"] >= start_date)
            & (self.raw_data["datetime"] <= end_date)
        ].copy()

        return raw_data_filtered
