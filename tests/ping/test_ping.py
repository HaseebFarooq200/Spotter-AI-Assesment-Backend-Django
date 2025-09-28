from rest_framework import status

from system_admin.utils import print_test_failed, print_test_header, print_test_passed
from ..test_setup import TestSetUp


class PingTest(TestSetUp):
    # ?###################################################
    # ?    TEST : SERVER PING PONG
    # ?###################################################
    def test_ping_pong(self):
        print_test_header("ping-pong")

        url = "/api/ping"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = response.data

        self.assertEqual(json_data["Status"], "success")
        self.assertEqual(json_data["Message"], "pong")
        print_test_passed()
