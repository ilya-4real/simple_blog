from django.test import TestCase
from ..forms import UserSignUpForm


class TestForms(TestCase):
    def test_with_valid_data(self):
        form = UserSignUpForm(data={
            'username': 'exampleusername',
            'email': 'example@mail.com',
            'password1': 'passww112233@',
            'password2': 'passww112233@',
        })

        self.assertTrue(form.is_valid())

    def test_with_no_data(self):
        form = UserSignUpForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
