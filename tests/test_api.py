import unittest
from app.views import app


class APITest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_vessel_invalid_data(self):
        response = self.app.get("/api/vessel_invalid_data/3001")
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_vessel_data(self):
        response = self.app.get("/api/vessel_invalid_data/9999")  # Invalid vessel code
        self.assertEqual(response.status_code, 404)

    def test_invalid_input_format(self):
        response = self.app.get(
            "/api/vessel_invalid_data/notanumber"
        )  # Invalid vessel code format
        self.assertEqual(response.status_code, 400)

    def test_vessel_speed_difference(self):
        response = self.app.get(
            "/api/vessel_speed_difference/3001"
        )  # Valid vessel code
        self.assertEqual(response.status_code, 200)

    def test_vessel_compliance_comparison(self):
        response = self.app.get(
            "/api/vessel_compliance_comparison/19310/3001"
        )  # Valid vessel codes
        self.assertEqual(response.status_code, 200)

    def test_compliance_comparison_invalid_vessels(self):
        response = self.app.get(
            "/api/vessel_compliance_comparison/9999/8888"
        )  # Invalid vessel codes
        self.assertEqual(response.status_code, 404)

    def test_compliance_comparison_invalid_input_format(self):
        response = self.app.get(
            "/api/vessel_compliance_comparison/3001/notanumber"
        )  # Invalid vessel code format
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
