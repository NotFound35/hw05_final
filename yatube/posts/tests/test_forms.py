from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import CommentForm, PostForm
from ..models import Comment, Group, Post

User = get_user_model()


class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        # cls.post = Post.objects.create(
        #     text='test-text',
        #     author=cls.user
        # )
        cls.group = Group.objects.create(
            title='title',
            slug='slug',
            description='description'
        )

    def setUp(self):
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_create_post_form(self):
        post_count = Post.objects.count()
        response = self.auth_user.post(
            reverse('posts:post_create'),
            data={
                'text': 'TestText',
                'group': self.group.id,
                'author': self.user
            },
            follow=True
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('posts:profile',
                                               kwargs={'username': self.user}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        post = Post.objects.first()
        self.assertEqual(post.text, 'TestText')
        self.assertEqual(post.group, self.group)
        self.assertEqual(post.author, self.user)


    def test_edit_post_form(self):
        post = Post.objects.create(
            text='TestText',
            group=self.group,
            author=self.user
        )
        group_2 = Group.objects.create(
            title='NewGroup',
            slug='NewSlug',
            description='NewDescription'
        )
        post_count = Post.objects.count()
        # form_data = {
        #     'text': 'test-text',
        #     'group': self.group.id
        # }

        response = self.auth_user.post(
            reverse('posts:post_edit', args=(post.id,)),
            data={
                'text': 'NewText',
                'group': group_2.id
            },
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), post_count)
        post = Post.objects.first()
        self.assertEqual(post.text, 'NewText')
        self.assertEqual(post.author, self.user),
        self.assertEqual(post.group, group_2)


class CommentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.form = CommentForm()
        cls.user = User.objects.create_user(username='auth2')
        cls.post = Post.objects.create(
            text='test-text',
            author=cls.user
        )
        cls.comment = Comment.objects.create(
            text='CommentText',
            author=cls.user,
            post=CommentTest.post
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_create_comment_form(self):
        comment_count = Comment.objects.count()
        response = self.auth_user.post(
            reverse('posts:add_comment', args=[self.post.id]),
            data={
                'text': 'CommentText',
                'author': self.user
            },
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}
        ))
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.text, 'CommentText')
        self.assertEqual(comment.author, self.user)
