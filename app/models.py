import pandas as pd


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
        # Specify columns to check for invalid data to avoid checking
        # lat/long, vessel_code and timestamp columns
        columns = [
            "power",
            "fuel_consumption",
            "actual_speed_overground",
            "proposed_speed_overground",
            "predicted_fuel_consumption",
        ]

        self.invalid_data.clear()
        valid_mask = pd.Series([True] * len(self.data))

        for column in columns:
            # Conditions for invalid data
            below_zero = self.data[column] < 0
            missing_value = self.data[column].isna()

            for condition, problem_type in [
                (below_zero, "below_zero"),
                (missing_value, "missing_value"),
            ]:
                # Update valid mask
                valid_mask &= ~condition

                # Aggregate invalid data by 'vessel_code'
                invalid_rows = self.data[condition]
                if not invalid_rows.empty:
                    summary = invalid_rows.groupby("vessel_code").size().to_dict()
                    for vessel_code, count in summary.items():
                        self.invalid_data.setdefault(vessel_code, {}).setdefault(
                            problem_type, {}
                        ).setdefault(column, 0)
                        self.invalid_data[vessel_code][problem_type][column] += count

        # Filter out invalid data based on the updated valid mask
        self.data = self.data[valid_mask]

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
