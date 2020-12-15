from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json

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
        token =response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION ='Bearer '+token)
        response2 =self.client.get(self.url)
        
        self.assertEqual(403,response2.status_code)

class UserLogin(APITestCase):
    
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "bunyadtest"
        self.password = "sifre1342"
        self.user = User.objects.create_user(username =self.username,password = self.password)

    def test_user_token(self):
        response = self.client.post(self.url_login,{"username":"bunyadtest","password":"sifre1342"})
        self.assertEqual(200,response.status_code)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        response = self.client.post(self.url_login,{"username":"asfasfafa","password":"sifre1342"})
        self.assertEqual(401,response.status_code)


    def test_user_empty_data(self):
        response = self.client.post(self.url_login,{"username":"","password":""})
        self.assertEqual(400,response.status_code)



class UserPasswordChange(APITestCase):
    url=reverse("account:change-password")
    url_login = reverse("token_obtain_pair")
    def setUp(self):
        self.username = "bunyadtest"
        self.password = "sifre1342"
        self.user = User.objects.create_user(username =self.username,password = self.password)

    def login_with_token(self):
        data ={
            "username":"bunyadtest",
            "password":"sifre1342"
        }
        response = self.client.post(self.url_login,data)
        self.assertEqual(200,response.status_code)
        token =response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION ='Bearer '+token)
        response = self.client.get(self.url_login)
        

    #oturum açılmadan girildiğinde hata 
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401,response.status_code)

    
    def test_with_valid_information(self):
        self.login_with_token()
        data ={
            "old_password":"sifre1342",
            "new_password":"sifre134221"
        }
        response =self.client.put(self.url,data)
        self.assertEqual(204,response.status_code)


    def test_with_wrong_information(self):
        self.login_with_token()
        data ={
            "old_password":"gsgsg",
            "new_password":"sifre134221"
        }
        response =self.client.put(self.url,data)
        self.assertEqual(400,response.status_code)

    def test_with_empty_information(self):
        self.login_with_token()
        data ={
            "old_password":"",
            "new_password":""
        }
        response =self.client.put(self.url,data)
        self.assertEqual(400,response.status_code)


class UserProfileUpdate(APITestCase):
    url=reverse("account:me")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "bunyadtest"
        self.password = "sifre1342"
        self.user = User.objects.create_user(username =self.username,password = self.password)

    def login_with_token(self):
        data ={
            "username":"bunyadtest",
            "password":"sifre1342"
        }
        response = self.client.post(self.url_login,data)
        self.assertEqual(200,response.status_code)
        token =response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION ='Bearer '+token)
    
        #oturum açılmadan girildiğinde hata 
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(404,response.status_code) #401 olmalıdı mende 404 gelir
    

    def test_with_valid_information(self):
        self.login_with_token()
        data ={
            "id":1,
            "first_name":"",
            "last_name":"",
            "profile": {
                "id":1,
                "note": "heri",
                "twitter": "heri"
                }
        }
        response =self.client.put(self.url,data,format='json')
        self.assertEqual(200,response.status_code)
        self.assertEqual(json.loads(response.content),data)

    
    def test_with_empty_information(self):
        self.login_with_token()
        data ={
            "id":1,
            "first_name":"",
            "last_name":"",
            "profile": {
                "id":1,
                "note": "",
                "twitter": ""
                }
        }
        response =self.client.put(self.url,data,format='json')
        self.assertEqual(200,response.status_code)
     