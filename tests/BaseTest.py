import unittest
import logging
import urllib.parse
import requests
from api import create_app


class BaseTest(unittest.TestCase):
    def setUp(self):
        # app = create_app('config.settings.DevelopmentConfig')
        # app.run(host="0.0.0.0", port=8888, threaded=True, use_debugger=True)
        self.ok_code = (200, 201, 202, 203, 204)
        super(BaseTest, self).setUp()

    def tearDown(self):
        super(BaseTest, self).tearDown()

    def fetch_request(self, path, **arvgs):
        response = None
        params = arvgs.get("params", {})
        # params = urllib.parse.urlencode(arvgs["params"])
        method = arvgs.get("method", "get")
        if method.lower() == "post":
            response = requests.post(path, data=params)

        elif method.lower() == "get":
            response = requests.get(path, params=params)

        elif method.lower() == "put":
            response = requests.put(path, data=params)

        elif method.lower() == "delete":
            response = requests.delete(path, params=params)

        elif method.lower() == "patch":
            response = requests.patch(path, data=params)

        result = response.status_code
        print(response.text)
        logging.warning(result)
        return result
