from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from accounts.views import UserLogIn, SignUp, log_out_user, ProfileUpdateView, UserProfile1


class TestAccountsUrls(SimpleTestCase):
    def test_login_url(self):
        url = reverse('log_in_url')
        self.assertEquals(resolve(url).func.view_class, UserLogIn)

    def test_logout_url(self):
        url = reverse('log_out_url')
        self.assertEquals(resolve(url).func, log_out_user)

    def test_signup_url(self):
        url = reverse('sign_up_url')
        self.assertEquals(resolve(url).func.view_class, SignUp)

    def test_profile_update_url(self):
        url = reverse('user_update_url')
        self.assertEquals(resolve(url).func.view_class, ProfileUpdateView)

    def test_profile_url(self):
        url = reverse('user_profile_url', args=['1'])
        self.assertEquals(resolve(url).func.view_class, UserProfile1)


class TestAccountsViews(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_login_view(self):
        url = reverse('log_in_url')
        response = self.client.get(url)
        print(response)
        print(dir(response))
        print(response.content.decode())
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'accounts/log_in.html')
