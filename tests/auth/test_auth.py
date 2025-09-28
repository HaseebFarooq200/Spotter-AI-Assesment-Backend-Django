from rest_framework import status

from system_admin.utils import print_test_failed, print_test_header, print_test_passed
from ..test_setup import TestSetUp


class TokenRefreshUnitTest(TestSetUp):
    # ---------------------------------------------------------------------------- #
    #                                  UNIT TESTS                                  #
    # ---------------------------------------------------------------------------- #

    def do_register(self, request_data):
        print_test_header("register")

        url = f"/api/register/"
        response = self.client.post(url, data=request_data)
        print_test_passed()

        return response

    def do_token_refresh(self, request_data):
        print_test_header("token-refresh")

        url = f"/api/token/refresh/"
        response = self.client.post(url, data=request_data)
        print_test_passed()
        return response

    def do_logout(self):
        print_test_header("logout")

        url = f"/api/logout/"
        response = self.client.post(url, headers=self.headers)
        print_test_passed()
        return response


class TokenRefreshTest(TokenRefreshUnitTest):
    # ?###################################################
    # ?              TESTS - CASES
    # ?###################################################

    def test_refresh_token(self):
        # FAILED (no/wrong token)
        response = self.do_token_refresh({})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_data = {
            "refresh": None,
        }
        response = self.do_token_refresh(request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # SUCCESS
        request_data = {
            "refresh": self.tokens["RefreshToken"],
        }
        response = self.do_token_refresh(request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # FAILED (old token)
        request_data = {
            "refresh": self.tokens["RefreshToken"],
        }
        response = self.do_token_refresh(request_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        self.headers["RefreshToken"] = self.tokens["RefreshToken"]

        response = self.do_logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register(self):
        request_data = {
            "Email": "auth_test@test.com",
            "FirstName": "john",
            "LastName": "doe",
            "DateOfBirth": "1995-07-27",
            "password": "123456789",
        }
        response = self.do_register(request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.do_register(request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.custom_login("auth_test@test.com", "123456789")
        self.test_refresh_token()

        self.custom_login("auth_test@test.com", "123456789")
        self.test_logout()
