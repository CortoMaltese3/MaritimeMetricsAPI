import pandas as pd
from scipy import stats


class MaritimeData:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = self._load_csv()
        self.invalid_data = {}  # Store problems and their types
        print(f"Original dataset size: {len(self.data)}")
        if not self.data.empty:
            self._filter_invalid_data()
            print(f"Filtered dataset size: {len(self.data)}")

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

    def _filter_by_condition(self, condition_func, problem_type, columns):
        for column in columns:
            mask = condition_func(self.data[column])
            self.data.loc[mask, column] = pd.NA
            invalid_rows = self.data[mask]
            if not invalid_rows.empty:
                summary = invalid_rows.groupby("vessel_code").size().to_dict()
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
