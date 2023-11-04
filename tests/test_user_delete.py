from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):

    def setup(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.user_id = self.get_json_value(response, "id")


    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.asser_content_decode(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")


    def test_delete_user_successfully(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        response3 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_headers(response3, "x-csrf-token")
        user_id = self.get_json_value(response3, "user_id")

        response4 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 200)

        response5 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response5, 404)
        Assertions.asser_content_decode(response5, "User not found")


    def test_delete_user_by_another_user(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        response6 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response6, "auth_sid")
        token = self.get_headers(response6, "x-csrf-token")

        register_data = self.prepare_registration_data()
        response7 = MyRequests.post("/user/", data=register_data)

        user_id = self.get_json_value(response7, "id")


        response8 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response8, 400)

