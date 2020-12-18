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

class FavouriteUpdateDelete(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "bunyadtest"
        self.password = "test2124s43"
        self.user =User.objects.create_user(username =self.username,password = self.password)
        self.user2 =User.objects.create_user(username ="bunyad1234",password = self.password)
        self.test_jwt_authentication()
        self.post  =Post.objects.create(title="Başlık",content="İçerik",user=self.user)
        self.favourite =Favourite.objects.create(content="deneme",post=self.post,user =self.user)
        self.url = reverse("favourite:update-delete",kwargs={"pk":self.favourite.pk })

    def test_jwt_authentication(self,username = "bunyadtest",password= "test2124s43"):
        response = self.client.post(self.url_login,data={"username":username,"password":password})
        self.assertEqual(200,response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token =response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+ self.token)

    def test_fav_delete(self):
        response=self.client.delete(self.url)
        self.assertEqual(204,response.status_code)

    def test_fav_delete_different_user(self):
        self.test_jwt_authentication("bunyad1234")
        response =self.client.delete(self.url)
        self.assertEqual(403,response.status_code)

    def test_fav_update(self):
        data ={
            "content":"içerik",
        }
        response =self.client.put(self.url,data)
        self.assertEqual(200,response.status_code)
        self.assertTrue(Favourite.objects.get(id=self.favourite.id).content == data["content"])


    def test_fav_update_diff_user(self):
        self.test_jwt_authentication("bunyad1234")
        data ={
            "content":"içerik 123",
            "user":self.user2.id
        }
        response = self.client.put(self.url,data)
        self.assertEqual(403,response.status_code)

    def test_unautherization(self):
        self.client.credentials()
        
        response = self.client.get(self.url)
        self.assertEqual(401,response.status_code)