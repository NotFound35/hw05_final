from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()


class TestCache(TestCase):
    """Проверка кэша"""
    def test_cache(self):
        response = self.client.get(reverse('posts:main_page'))
        self.assertEqual(len(response.context['page_obj']), 0)
        user = User.objects.create_user(username='auth')
        Post.objects.create(
            text='TestText',
            author=user
        )
        self.assertEqual(len(response.context['page_obj']), 0)
        cache.clear()
        self.assertEqual(len(response.context['page_obj']), 0)