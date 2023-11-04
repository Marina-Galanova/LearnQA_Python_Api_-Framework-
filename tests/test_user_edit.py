from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def setup(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.user_id = self.get_json_value(response, "id")

    def test_edit_just_created_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_user_by_unauthorized_user(self):
        response5 = MyRequests.put(
            f"/user/{self.user_id}",
            data={"firstName": "test"}
        )

        Assertions.assert_code_status(response5, 400)
        Assertions.asser_content_decode(response5, "Auth token not supplied")


    def test_edit_user_by_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response6 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response6, "auth_sid")
        token = self.get_headers(response6, "x-csrf-token")

        response7 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "test"}
        )

        Assertions.assert_code_status(response7, 400)
        Assertions.asser_content_decode(response7, "Please, do not edit test users with ID 1, 2, 3, 4 or 5.")


    def test_edit_user_with_incorrect_email(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        response8 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response8, "auth_sid")
        token = self.get_headers(response8, "x-csrf-token")

        response9 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": "testexample.com"}
        )

        Assertions.assert_code_status(response9, 400)
        Assertions.asser_content_decode(response9, "Invalid email format")

    def test_edit_user_with_short_firstName(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        response10 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response10, "auth_sid")
        token = self.get_headers(response10, "x-csrf-token")

        response11 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "1"}
        )

        Assertions.assert_code_status(response11, 400)
        Assertions.asser_content_decode(response11, '{"error":"Too short value for field firstName"}')
