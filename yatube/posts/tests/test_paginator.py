from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User

from yatube.settings import POST_COUNT

POSTS = 15

POST_PAGE_2_CNT = 6

POST_PAGE_3_CNT = 5


class PaginatorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='title',
            slug='slug',
            description='description'
        )
        posts = [
            Post(
                text=f'text{i}',
                author=cls.user,
                group=cls.group
            ) for i in range(POSTS)
        ]
        Post.objects.bulk_create(posts)

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(self.user)

    def test_first_main_page_correct(self):
        response = self.auth_client.get(reverse('posts:main_page'))
        self.assertEqual(len(response.context['page_obj']), POST_COUNT)

    def test_second_main_page_correct(self):
        response = self.auth_client.get(reverse('posts:main_page') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), POST_PAGE_2_CNT)

    def test_first_group_list_correct(self):
        response = self.auth_client.get(reverse('posts:group_list',
                                                kwargs={'slug': 'slug'}))
        self.assertEqual(len(response.context['page_obj']), POST_COUNT)

    def test_second_group_list_correct(self):
        response = self.auth_client.get(reverse(
                                        'posts:group_list',
                                        kwargs={'slug': 'slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), POST_PAGE_3_CNT)

    def test_first_profile_page_correct(self):
        response = self.auth_client.get(reverse('posts:profile',
                                                kwargs={'username': self.user}
                                                ))
        self.assertEqual(len(response.context['page_obj']), POST_COUNT)

    def test_second_profile_page_correct(self):
        response = self.auth_client.get(reverse(
                                        'posts:profile',
                                        kwargs={'username': self.user}
                                        ) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), POST_PAGE_3_CNT)
