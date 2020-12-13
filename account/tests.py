from rest_framework.test import APITestCase
from django.urls import reverse
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")
    url_login = reverse("token_obtain_pair")
    def test_user_registration(self):
        """
        Doğru veriler ile kayıt işlem
        """
        data = {
            "username":"bunyadtestsa",
            "password":"bunyadtest1257"
        }

        response = self.client.post(self.url,data=data)
        self.assertEqual(201,response.status_code)

    def test_user_invalid_password(self):
        """
        hatalı şifre ile login olamama
        """
        data = {
            "username":"bunyadtest",
            "password":"12"
        }

        response = self.client.post(self.url,data=data)
        self.assertEqual(400,response.status_code)

    def test_unique_name(self):
        """
        Aynı kullanıcı ile yeni kayıt oluşturama ma
        """
        self.test_user_registration()
        data = {
            "username":"bunyadtestsa",
            "password":"bunyadtest1257"
        }

        response = self.client.post(self.url,data=data)
        self.assertEqual(400,response.status_code)

    def test_user_authentiacated_registration(self):
        """
        session ile giriş yapmış veriler ile kayıt işlem
        """
        self.test_user_registration()
       
        self.client.login(username ='bunyadtestsa',password='bunyadtest1257')
        response  =self.client.get(self.url)
        
        self.assertEqual(403,response.status_code)

    def test_user_authentiacated_token_registration(self):
        """
        token ile giriş yapmış veriler ile kayıt işlem
        """
        self.test_user_registration()

        data = {
            "username":"bunyadtestsa",
            "password":"bunyadtest1257"
        }
        response = self.client.post(self.url_login,data)
        self.assertEqual(200,response.status_code)
        print(response.data["access"])
        token =response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION ='Bearer '+token)
        response2 =self.client.get(self.url)
        
        self.assertEqual(403,response2.status_code)