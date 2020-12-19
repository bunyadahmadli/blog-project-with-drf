from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from post.models import Post
from post.models import Post
import json

class PostCreateList(APITestCase):
    url_create = reverse("post:create")
    url_list = reverse("post:posts")
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

    def test_add_new_post(self):
        data ={
            "title":"baslık",
            "content":"icerik"
        }
        repsonse =self.client.post(self.url_create,data)
        self.assertEqual(201,repsonse.status_code)

    def test_add_new_post_unauthorization(self):
        self.client.credentials()
        data ={
            "title":"baslık",
            "content":"icerik"
        }
        self.client.credentials()
        repsonse =self.client.post(self.url_create,data)
        self.assertEqual(201,repsonse.status_code) #normalde 401 olmalıdı giriş olmamış deşiklik işlemedi
    

    def test_posts(self):
        self.test_add_new_post()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)["results"])==Post.objects.all().count())