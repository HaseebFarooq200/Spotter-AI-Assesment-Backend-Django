from rest_framework import status

from system_admin.utils import print_test_failed, print_test_header, print_test_passed
from ..test_setup import TestSetUp


class UserUnitTest(TestSetUp):
    # ?###################################################
    # ?                  UNIT - TESTS
    # ?###################################################

    def do_create_user(self, request_body):
        print_test_header("create_user")

        url = "/api/users/"

        response = self.client.post(url, headers=self.headers, data=request_body)

        if response.status_code == status.HTTP_201_CREATED:
            print_test_passed()
        else:
            print(response.content)
            print_test_failed()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def do_get_users_list(self):
        print_test_header("get_users_list")

        url = f"/api/users/"

        response = self.client.get(url, headers=self.headers)

        if response.status_code == status.HTTP_200_OK:
            print_test_passed()
        else:
            print(response.content)
            print_test_failed()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def do_get_one_user(self, user_id):
        print_test_header("get_one_user")

        url = f"/api/users/{user_id}/"

        response = self.client.get(url, headers=self.headers)

        if response.status_code == status.HTTP_200_OK:
            print_test_passed()
        else:
            print(response.content)
            print_test_failed()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def do_update_one_user(self, user_id, request_body):
        print_test_header("update_user")

        url = f"/api/users/{user_id}/"

        response = self.client.put(url, headers=self.headers, data=request_body)

        if response.status_code == status.HTTP_200_OK:
            print_test_passed()
        else:
            print(response.content)
            print_test_failed()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def do_delete_one_user(self, user_id):
        print_test_header("delete_user")

        url = f"/api/users/{user_id}/"

        response = self.client.delete(url, headers=self.headers)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            print_test_passed()
        else:
            print(response.content)
            print_test_failed()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserTest(UserUnitTest):
    # ?###################################################
    # ?              TESTS - CASES
    # ?###################################################

    def test_user_crud_api(self):
        # CREATE
        request_body = {
            "Email": "test@test.com",
            "FirstName": "john",
            "LastName": "doe",
            "DateOfBirth": "1995-07-27",
            "password": "123456789",
        }

        json_data = self.do_create_user(request_body)
        self.assertEqual(json_data["Email"], request_body["Email"])
        self.assertEqual(json_data["FirstName"], request_body["FirstName"])
        self.assertIn("DateOfBirth", json_data)

        # READ
        json_data = self.do_get_users_list()
        self.assertGreater(json_data["count"], 0)
        self.assertGreater(len(json_data["results"]), 0)
        self.assertIn("UserID", json_data["results"][0])
        self.assertIn("Email", json_data["results"][0])
        self.assertIn("FirstName", json_data["results"][0])
        self.assertIn("LastName", json_data["results"][0])
        self.assertIn("CreatedAt", json_data["results"][0])
        self.assertIn("UpdatedAt", json_data["results"][0])

        test_user_id = json_data["results"][len(json_data["results"]) - 1][
            "UserID"
        ]  # last user

        json_data = self.do_get_one_user(test_user_id)
        self.assertIn("UserID", json_data)
        self.assertIn("Email", json_data)
        self.assertIn("FirstName", json_data)
        self.assertIn("LastName", json_data)
        self.assertIn("CreatedAt", json_data)
        self.assertIn("UpdatedAt", json_data)

        # UPDATE
        request_body["LastName"] = "snow"
        json_data = self.do_update_one_user(test_user_id, request_body)
        self.assertEqual(request_body["Email"], json_data["Email"])
        self.assertEqual(request_body["FirstName"], json_data["FirstName"])
        self.assertEqual(request_body["LastName"], json_data["LastName"])

        # DELETE
        self.do_delete_one_user(test_user_id)
