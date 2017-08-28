import unittest
from tests.BaseTest import BaseTest


class TestUser(BaseTest):
    def test_example(self):
        params = {"user": "lifei", "passwd": "123"}
        result = self.fetch_request("http://127.0.0.1:8888/api/login", method="post", params=params)
        self.assertIn(result, self.ok_code)


if __name__ == "__main__":
    unittest.main()


