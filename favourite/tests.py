from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from post.models import Post
from favourite.models import Favourite
import json
class FavouriteCreateList(APITestCase):
    url = reverse("favourite:create")
    url_login = reverse("token_obtain_pair")
    
    def setUp(self):
        self.username = "bunyadtest"
        self.password = "test2124s43"
        
        self.user =User.objects.create_user(username =self.username,password = self.password)
        self.test_jwt_authentication()
        self.post  =Post.objects.create(title="Başlık",content="İçerik",user=self.user)

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login,data={"username":self.username,"password":self.password})
        self.assertEqual(200,response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token =response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+ self.token)

    def test_add_favourite(self):
        
        data ={
            "content":"içerik güzel",
            "user":self.user.id,
            "post":self.post.id
        }

        response = self.client.post(self.url,data)
        self.assertEqual(201,response.status_code)

    def test_user_favs(self):
        self.test_add_favourite()
        response =self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)["results"])==
        Favourite.objects.filter(user=self.user).count())