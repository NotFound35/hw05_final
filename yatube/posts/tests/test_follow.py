from django.test import Client, TestCase
from django.urls import reverse
from ..models import User
from ..models import Follow


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
        follow_count = Follow.objects.all().count()
        self.client1.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.author.username}
            )
        )
        self.assertEqual(Follow.objects.all().count(), follow_count + 1)

    def test_unfollow(self):
        follow_cnt = Follow.objects.all().count()
        self.client2.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.author.username}
            )
        )
        self.assertEqual(Follow.objects.all().count(), follow_cnt)
