"""
Module defining the data models and business logic for the maritime data application.

Includes classes and methods for loading and processing maritime data, such as
filtering invalid data, calculating compliance scores, and comparing vessel metrics.
The primary class, `MaritimeData`, encapsulates the logic for data handling, including
loading from CSV, data cleansing, and metrics computation.
"""

import logging
from typing import Any, Dict, List

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from scipy import stats


class MaritimeData:
    """
    Manages maritime data operations, including loading, filtering, and processing vessel data.

    The class provides functionality to load vessel data from a CSV file, apply several filters
    to clean the data, and calculate metrics for vessels over specified periods.

    :param csv_path: Path to the CSV file containing maritime data.
    :type csv_path: str
    """

    def __init__(self, csv_path: str) -> None:
        """
        Initializes the MaritimeData class with the path to the data CSV.
        """
        self.csv_path = csv_path
        # Load raw data from CSV
        self.raw_data = self._load_csv()
        # Create a copy of raw data to apply filters and preserve the original data
        self.filtered_data = self.raw_data.copy()
        # Store information about invalid data to be used in the API
        self.invalid_data = {}
        logging.info(f"Original dataset size: {len(self.raw_data)}")
        if not self.raw_data.empty:
            # Apply data cleansing filters
            self._filter_invalid_data()
            logging.info(f"Filtered dataset size: {len(self.filtered_data)}")

    def _load_csv(self) -> pd.DataFrame:
        """
        Loads maritime data from a CSV file.

        Attempts to read the maritime data CSV file into a pandas DataFrame. If the file
        is not found, or another exception occurs during loading, it handles the exception
        gracefully by printing an error message and returning an empty DataFrame.

        :return: A DataFrame with the loaded maritime data, or an empty DataFrame if
                the file cannot be loaded.
        :rtype: pd.DataFrame
        """
        try:
            df = pd.read_csv(self.csv_path, parse_dates=["datetime"])
            return df
        except FileNotFoundError:
            logging.error("CSV file not found.")
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"An unexpected error occurred while loading CSV: {e}")
            return pd.DataFrame()

    def _filter_invalid_data(self) -> None:
        """
        Applies a series of data cleansing filters to the loaded maritime data.

        This method sequentially calls other methods to filter out rows based on
        specific criteria: values below zero, missing values, statistical outliers,
        and invalid geocoordinates. This process cleans the dataset, preparing it
        for further analysis and usage within the application.

        :return: None
        """
        self._filter_below_zero()
        self._filter_missing_values()
        self._filter_outliers()
        self._filter_invalid_geocoordinates()

    def _filter_below_zero(self) -> None:
        """
        Filters out records with negative values in specified numerical columns.

        Identifies and removes rows from `self.filtered_data` where values in critical
        numerical columns such as power, fuel consumption, and speed over ground are
        below zero, as these values are considered invalid for the dataset's context.

        The columns checked are: 'power', 'fuel_consumption', 'actual_speed_overground',
        'proposed_speed_overground', and 'predicted_fuel_consumption'.

        :return: None
        """
        # Define the condition for filtering out rows where the specified columns are below zero.
        # We specify these columns to avoid filtering out lat/long values that could be valid.
        try:

            def get_below_zero(column):
                """Get rows with values below zero in the specified column."""
                return column < 0

            columns = [
                "power",
                "fuel_consumption",
                "actual_speed_overground",
                "proposed_speed_overground",
                "predicted_fuel_consumption",
            ]
            self._filter_by_condition(get_below_zero, "below_zero", columns=columns)
        except Exception as e:
            logging.error(f"Error filtering below zero: {e}")

    def _filter_missing_values(self) -> None:
        """
        Removes records with missing (NA) values in critical columns.

        Targets specific columns for checking missing values, including vessel identifiers,
        timestamps, geocoordinates, and various performance metrics. Rows with any missing
        values in these columns are considered incomplete and are removed from the dataset.

        Target columns: 'vessel_code', 'datetime', 'latitude', 'longitude', 'power',
        'fuel_consumption', 'actual_speed_overground', 'proposed_speed_overground',
        and 'predicted_fuel_consumption'.

        :return: None
        """

        # Define the condition for filtering out rows where the specified columns have
        # missing values.
        try:

            def get_missing_columns(col):
                return col.isna()

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

            self._filter_by_condition(
                get_missing_columns, "missing_value", columns=columns
            )
        except Exception as e:
            logging.error(f"Failed to filter missing values: {e}")

    def _filter_outliers(self) -> None:
        """
        Identifies and removes outliers based on Z-scores in specified numerical columns.

        Applies a statistical method to detect and exclude outliers from the dataset. An
        outlier is defined as a data point that is more than two standard deviations away
        from the mean. This method ensures the data's consistency by retaining only values
        within a reasonable range, enhancing the reliability of subsequent analyses.

        Outlier detection is applied to columns: 'power', 'fuel_consumption',
        'actual_speed_overground', 'proposed_speed_overground', and 'predicted_fuel_consumption'.

        :return: None
        """
        # Define the condition for filtering out rows where the specified columns have outliers.
        # z-scores can be adjusted depending on the situation.
        # We specify these columns to only apply filtering in numerical columns.
        try:
            columns = [
                "power",
                "fuel_consumption",
                "actual_speed_overground",
                "proposed_speed_overground",
                "predicted_fuel_consumption",
            ]
            for column in columns:
                # Check if the column exists and is numerical (rule out strings and mixed types)
                if (
                    column in self.filtered_data.columns
                    and self.filtered_data[column].dtype != "object"
                ):
                    # dropna() ensures no NaN values are included in the z-score calculation
                    # This can be adjusted depending on how strict we want to be.
                    # Leave it as 2 for now.
                    z_scores = stats.zscore(self.filtered_data[column].dropna())
                    outlier_mask = abs(z_scores) > 2

                    # Create a mask that aligns with the original data with the default value
                    # set to False
                    full_mask = pd.Series(False, index=self.filtered_data.index)
                    # Update the mask with the outlier values
                    non_na_indices = self.filtered_data[column].dropna().index
                    # Ensure alignment with the original data
                    full_mask.loc[non_na_indices] = outlier_mask

                    # Apply the mask using the defined function
                    self._filter_by_condition(
                        lambda col: full_mask, "outlier", [column]
                    )
        except Exception as e:
            logging.error(f"Failed to filter outliers: {e}")

    def _filter_invalid_geocoordinates(self) -> None:
        """
        Filters out records with geocoordinate values outside valid global ranges.

        Validates latitude and longitude values by ensuring they fall within the
        acceptable global range: latitudes between -90 and 90, and longitudes
        between -180 and 180 degrees. Records outside these ranges are considered
        invalid and are removed, improving the geographic data's accuracy.

        :return: None
        """
        try:

            def get_invalid_latitude(col):
                """Get rows with invalid latitude values."""
                return (col < -90) | (col > 90)

            def get_invalid_longitude(col):
                """Get rows with invalid longitude values."""
                return (col < -180) | (col > 180)

            self._filter_by_condition(
                get_invalid_latitude, "invalid_latitude", ["latitude"]
            )
            self._filter_by_condition(
                get_invalid_longitude, "invalid_longitude", ["longitude"]
            )
        except Exception as e:
            logging.error(f"Failed to filter invalid geocoordinates: {e}")

    def _filter_by_condition(
        self, condition_func: Any, problem_type: str, columns: List[str]
    ) -> None:
        """
        Applies a filtering condition to specified columns and updates invalid data tracking.

        This generic method applies a given condition to filter data across specified columns,
        updates the filtered data, and logs details of filtered records by problem type and
        vessel code.

        :param condition_func: A function defining the condition to filter the data by.
        :param problem_type: A description of the problem type for logging.
        :param columns: A list of column names to apply the filtering condition to.
        :return: None
        """
        try:
            for column in columns:
                mask = condition_func(self.filtered_data[column])
                valid_rows = self.filtered_data.loc[~mask]
                filtered_rows = self.filtered_data.loc[mask]

                # Update the main data with rows where the condition is not met.
                # Add this approach to filter out the invalid rows instead of marking them as 
                # invalid
                self.filtered_data = valid_rows

                if not filtered_rows.empty:
                    summary = filtered_rows.groupby("vessel_code").size().to_dict()
                    for vessel_code, count in summary.items():
                        self.invalid_data.setdefault(vessel_code, {}).setdefault(
                            problem_type, {}
                        ).setdefault(column, 0)
                        self.invalid_data[vessel_code][problem_type][column] += count
        except KeyError as e:
            logging.error(f"Column error in _filter_by_condition: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in _filter_by_condition: {e}")

    def get_invalid_data_for_vessel(
        self, vessel_code: int
    ) -> Dict[str, Dict[str, Dict[str, int]]]:
        """
        Retrieves a summary of invalid data entries for a specific vessel.

        Organizes invalid data entries by problem type and affected columns, providing
        a detailed breakdown of issues identified in the vessel's data.

        :param vessel_code: The unique identifier for the vessel.
        :return: A nested dictionary summarizing invalid data by problem type and column.
        :rtype: Dict[str, Dict[str, Dict[str, int]]]
        """
        sorted_summary = {}
        if vessel_code in self.invalid_data:
            vessel_summary = self.invalid_data[vessel_code]
            for problem_type, columns in vessel_summary.items():
                sorted_columns = sorted(
                    columns.items(), key=lambda x: x[1], reverse=True
                )
                sorted_summary[problem_type] = dict(sorted_columns)
        return sorted_summary

    def get_speed_differences_for_vessel(
        self, vessel_code: int
    ) -> List[Dict[str, Any]]:
        """
        Calculates the speed differences between actual and proposed speeds for a vessel.

        For each record pertaining to the specified vessel, computes the absolute difference
        between actual and proposed speeds over ground, adding these as a new metric.

        :param vessel_code: The unique identifier for the vessel.
        :return: A list of dictionaries, each containing latitude, longitude, and the calculated
                speed difference for a record.
        :rtype: List[Dict[str, Any]]
        """
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

    def calculate_compliance_score(self, vessel_code: int) -> float:
        """
        Computes a compliance score based on the deviation from proposed speeds.

        The score is an average percentage representing how closely the vessel's actual
        speed adheres to proposed speeds, with higher scores indicating closer adherence.

        :param vessel_code: The unique identifier for the vessel.
        :return: The compliance score as a float rounded to two decimal places.
        :rtype: float
        """
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

    def compare_vessel_compliance(self, vessel_code1: int, vessel_code2: int) -> str:
        """
        Compares the compliance scores of two vessels and indicates which is more compliant.

        Calculates compliance scores for both vessels based on their adherence to proposed speeds
        and returns a message comparing these scores.

        :param vessel_code1: Unique identifier for the first vessel.
        :param vessel_code2: Unique identifier for the second vessel.
        :return: Message indicating which vessel is more compliant or if they have eq compliance.
        :rtype: str
        """
        # Check if the vessel codes exist in the dataset
        if vessel_code1 not in self.filtered_data["vessel_code"].values:
            return f"Vessel code {vessel_code1} does not exist."

        if vessel_code2 not in self.filtered_data["vessel_code"].values:
            return f"Vessel code {vessel_code2} does not exist."

        score1 = self.calculate_compliance_score(vessel_code1)
        score2 = self.calculate_compliance_score(vessel_code2)

        if score1 > score2:
            message = (
                f"Vessel {vessel_code1} is more compliant with a compliance "
                f"score of {score1}% compared to Vessel {vessel_code2}'s "
                f"score of {score2}%."
            )
            return message
        if score2 > score1:
            message = (
                f"Vessel {vessel_code2} is more compliant with a compliance "
                f"score of {score2}% compared to Vessel {vessel_code1}'s "
                f"score of {score1}%."
            )
            return message
        return f"Both vessels have the same compliance score of {score1}%."

    def get_metrics_for_vessel_period(
        self, vessel_code: int, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieves filtered data metrics for a specific vessel over a given period.

        Metrics include calculated speed differences between actual and proposed speeds.
        If no data exists for the given period, an empty list is returned.

        :param vessel_code: Unique identifier for the vessel.
        :param start_date: Start of the period in 'YYYY-MM-DD' format.
        :param end_date: End of the period in 'YYYY-MM-DD' format.
        :return: List of dictionaries with data for each record within the period.
        :rtype: List[Dict[str, Any]]
        """
        # Check if datetime column is in the correct format
        if not is_datetime(self.filtered_data["datetime"]):
            logging.error("datetime column in incorrect format")
            return []

        filtered_data = self.filtered_data[
            (self.filtered_data["vessel_code"] == vessel_code)
            & (self.filtered_data["datetime"] >= start_date)
            & (self.filtered_data["datetime"] <= end_date)
        ].copy()

        if filtered_data.empty:
            logging.error("No data found for the specified vessel and period.")
            return []

        filtered_data["speed_difference"] = abs(
            filtered_data["actual_speed_overground"]
            - filtered_data["proposed_speed_overground"]
        )
        return filtered_data

    def get_raw_metrics_for_vessel_period(
        self, vessel_code: int, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieves raw data metrics for a specific vessel over a given period.

        Provides unfiltered access to data for in-depth analysis.
        but without applying any data cleansing or additional calculations.

        :param vessel_code: Unique identifier for the vessel.
        :param start_date: Start of the period in 'YYYY-MM-DD' format.
        :param end_date: End of the period in 'YYYY-MM-DD' format.
        :return: List of dictionaries with raw data for each record within the period.
        :rtype: List[Dict[str, Any]]
        """
        # Check if datetime column is in the correct format
        if not is_datetime(self.filtered_data["datetime"]):
            logging.error("datetime column in incorrect format")
            return []

        raw_data_filtered = self.raw_data[
            (self.raw_data["vessel_code"] == vessel_code)
            & (self.raw_data["datetime"] >= start_date)
            & (self.raw_data["datetime"] <= end_date)
        ].copy()

        return raw_data_filtered
