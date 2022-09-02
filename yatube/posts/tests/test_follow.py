from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class TestFollow(TestCase):
    """Проверка подписок"""
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='follower')
        cls.author = User.objects.create_user(username='following')
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass

    def setUp(self):
        self.client1 = Client()
        self.client1.force_login(self.user)
        self.client2 = Client()
        self.client2.force_login(self.author)

    def test_follow(self):
        follow_count = self.user.following.count()
        response = self.client2.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.author.username}
            )
        )
        self.assertRedirects(response, '/profile/following/')
        self.assertEqual(self.user.following.count(), follow_count)
