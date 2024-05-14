import unittest
from unittest.mock import patch
from job_data import query_keywords


class TestQueryKeywords(unittest.TestCase):

    @patch('job_data.requests.get')
    def test_successful_query(self, mock_get):
        # Mocking the response from the requests.get call
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": "data for keyword"}
        mock_get.return_value = mock_response

        # Test data
        api_url = 'http://api.example.com'
        app_id = 'test_app_id'
        api_key = 'test_api_key'
        keywords = ['test_keyword']

        # Calling the function
        result = query_keywords(api_url, app_id, api_key, keywords)

        # Check if the results are as expected
        self.assertIn('test_keyword', result)
        self.assertEqual(result['test_keyword'], {"results": "data for keyword"})

    @patch('job_data.requests.get')
    def test_api_error_response(self, mock_get):
        # Mocking a non-200 response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "not found"}
        mock_get.return_value = mock_response

        api_url = 'http://api.example.com'
        app_id = 'test_app_id'
        api_key = 'test_api_key'
        keywords = ['bad_keyword']

        # Calling the function
        result = query_keywords(api_url, app_id, api_key, keywords)

        # Check that the error is handled correctly
        self.assertIn('bad_keyword', result)
        self.assertTrue("Error: Received status code 404" in result['bad_keyword'])
