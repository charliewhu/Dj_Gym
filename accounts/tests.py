from django.test import TestCase
from django.conf import settings
from django.contrib import  auth 

# Create your tests here.

User = auth.get_user_model()

class UserTestCast(TestCase):

    def setUp(self): # create a user
        user_a = User(email='test@test.com')
        user_a_pw = 'some_123_password'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a #make available for other methods
        user_b = User.objects.create_user('test2@test.com', 'some_123_password')
        self.user_b = user_b
        superuser = User.objects.create_superuser(email='t@t.com', password='123')
        self.superuser = superuser

    def test_users_exist(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 3)
        self.assertNotEqual(user_count, 0) # not 0 users
        #print('user test complete')

    def test_usera_password(self):
        self.assertEqual(self.user_a.check_password('some_123_password'), True)

    def test_create_user(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')

    def test_user_a_perms(self):
        self.assertTrue(self.user_a.is_staff)
        self.assertTrue(self.user_a.is_superuser)
        self.assertFalse(self.user_a.is_admin)      

    def test_userb_perms(self):
        self.assertFalse(self.user_b.is_staff)
        self.assertFalse(self.user_b.is_superuser)
        self.assertFalse(self.user_b.is_admin)

    def test_superuser_perms(self):
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_admin)

    def test_user_password(self): 
        user_qs =  User.objects.filter(email__iexact='test@test.com') 
        self.assertTrue(
            self.user_a.check_password(self.user_a_pw)
            )
        self.assertFalse(
            self.user_a.check_password("fakepassword")
            )

    def test_login_url(self):
        login_url = settings.LOGIN_URL
        data = {"username": "test@test.com", "password": self.user_a_pw}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(status_code, 200)

    def test_login_success(self):
        self.client.login(email=self.user_a.email, password=self.user_a.password)
        print(User.objects.all()[0].is_authenticated )
        print(self.client.session)
        #self.assertIn(self.user_a.id, self.client.session)
