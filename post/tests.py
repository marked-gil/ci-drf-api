from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        """
        Automatically runs before every test method in the class
        """
        User.objects.create_user(username='marko', password='password1')

    def test_can_list_posts(self):
        marko = User.objects.get(username='marko')
        Post.objects.create(owner=marko, title='my title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='marko', password='password1')
        response = self.client.post('/posts/', {'title': 'my title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'my title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='password1')
        brian = User.objects.create_user(username='brian', password='password2')
        Post.objects.create(
            owner=adam, title='a title', content='content of adam'
        )
        Post.objects.create(
            owner=brian, title='another title', content='content of brian'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_fetch_post_by_invalid_id(self):
        response = self.client.get('/posts/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='password1')
        response = self.client.put('/posts/1/', {'title': 'updated title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'updated title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_cant_update_another_users_post(self):
        self.client.login(username='adam', password='password1')
        response = self.client.put('/posts/2/', {'title': 'me trying'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
