from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest

class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email 'vinkotov@example.com' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'testexample.com'
        data = self.prepare_registration_data(email)

        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 400)
        assert response1.content.decode("utf-8") == f"Invalid email format", \
             f"Unexpected response content {response1.content}"

    @pytest.mark.parametrize('field', [('email'), ('username'), ('password'), ('firstName'), ('lastName')])
    def test_create_user_without_any_field(self, field):
        data = self.prepare_registration_data_for_fields(field)
        response2 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"The following required params are missed: {field}", f"No required field {field}"

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data_short_name('1')
        response3 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == f"The value of 'username' field is too short", f"The value of 'username' field is too short"

    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data_short_name(251*'1')
        response4 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response4, 400)
        assert response4.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f"The value of 'username' field is too long"