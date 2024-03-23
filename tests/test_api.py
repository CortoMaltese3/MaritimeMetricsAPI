import unittest
from app.views import app


class APITest(unittest.TestCase):
    """
    Test suite for the Flask API endpoints.

    This class contains methods to test the functionality and response codes of the API
    endpoints under various conditions, including valid inputs, invalid inputs, and
    edge cases.
    """

    def setUp(self):
        """
        Set up the test client for Flask application.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_get_vessel_invalid_data(self):
        """
        Test retrieving invalid data summary for a valid vessel code.
        """
        response = self.app.get("/api/vessel_invalid_data/3001")
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_vessel_data(self):
        """
        Test invalid vessel code that results in a 404 not found response.
        """
        response = self.app.get("/api/vessel_invalid_data/9999")  # Invalid vessel code
        self.assertEqual(response.status_code, 404)

    def test_invalid_input_format(self):
        """
        Test retrieval with an invalid vessel code format, expecting a 400 error.
        """
        response = self.app.get("/api/vessel_invalid_data/notanumber")  # Invalid format
        self.assertEqual(response.status_code, 400)

    def test_vessel_speed_difference(self):
        """
        Test retrieving speed differences for a vessel with a valid code.
        """
        response = self.app.get("/api/vessel_speed_difference/3001")  # Valid code
        self.assertEqual(response.status_code, 200)

    def test_vessel_compliance_comparison(self):
        """
        Test compliance comparison between two vessels with valid codes.
        """
        response = self.app.get(
            "/api/vessel_compliance_comparison/19310/3001"
        )  # Valid codes
        self.assertEqual(response.status_code, 200)

    def test_compliance_comparison_invalid_vessels(self):
        """
        Test compliance comparison with invalid vessel codes, expecting a 404 error.
        """
        response = self.app.get(
            "/api/vessel_compliance_comparison/9999/8888"
        )  # Invalid codes
        self.assertEqual(response.status_code, 404)

    def test_compliance_comparison_invalid_input_format(self):
        """
        Test compliance comparison with an invalid vessel code format, expecting a 400 error.
        """
        response = self.app.get(
            "/api/vessel_compliance_comparison/3001/notanumber"
        )  # Invalid format
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
