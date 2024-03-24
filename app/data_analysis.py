"""This module contains the analyzing data. This will be used to cover the BONUS section of the assignment"""

import pandas as pd
from scipy import stats

from . import app

csv_path = app.config["CSV_PATH"]


class DataAnalyzer:
    """Analyzes data from a CSV file."""

    def __init__(self):
        """Initializes the DataAnalyzer with a DataFrame."""
        self.dataframe = pd.read_csv(csv_path)

    def detect_consecutive_problems(self, column_name, problem_type="missing_values"):
        """Identifies groups of consecutive waypoints with problematic data."""
        if problem_type == "missing_values":
            problem_mask = self.dataframe[column_name].isna()
        elif problem_type == "outliers":
            z_scores = stats.zscore(self.dataframe[column_name].dropna())
            problem_mask = abs(z_scores) > 2
        else:
            raise ValueError("Unsupported problem type specified.")

        # Identify consecutive groups with problems
        self.dataframe["problem_group"] = (
            problem_mask != problem_mask.shift()
        ).cumsum()
        problematic_groups = (
            self.dataframe[problem_mask].groupby("problem_group").size()
        )

        # Sort groups by size descending
        sorted_groups = problematic_groups.sort_values(ascending=False)
        return sorted_groups

    def get_problematic_data_summary(self, column_name, problem_type="missing_values"):
        """Returns a summary of problematic data groups for a specific column."""
        sorted_groups = self.detect_consecutive_problems(column_name, problem_type)

        # Convert sorted_groups Series to a dictionary with Python integers
        # to avoid JSON serialization issues
        groups_dict = sorted_groups.to_dict()
        groups_dict_converted = {key: int(value) for key, value in groups_dict.items()}

        summary = {
            "problem_type": problem_type,
            "column_name": column_name,
            "number_of_groups": len(sorted_groups),
            "largest_group_size": (
                int(sorted_groups.iloc[0]) if not sorted_groups.empty else 0
            ),
            "groups": groups_dict_converted,
        }
        return summary

    def filter_by_vessel(self, vessel_code):
        """Filters the dataframe for a specific vessel code."""
        self.dataframe = self.dataframe[self.dataframe["vessel_code"] == vessel_code]
