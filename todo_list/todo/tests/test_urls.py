from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from todo.models import Todo

User = get_user_model()


class TodoURLsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='User1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.todo = Todo.objects.create(title='Test title',
                                        description='Test description',
                                        author=self.user)

    def test_empty_url_redirect_to_index_page(self):

        response1 = self.guest_client.get('/')
        response2 = self.authorized_client.get('/')
        self.assertRedirects(response1, '/todos/')
        self.assertRedirects(response2, '/todos/', target_status_code=302)

    def test_urls_guest_client(self):
        """Access anonymous user."""
        pages = ('/todos/',
                 '/todos/sign_up/',
                 '/todos/sign_in/')
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                error_message = f'Error: no access to page {page}'
                self.assertEqual(200, response.status_code, error_message)

    def test_urls_redirect_guest_client(self):
        """Redirects anonymous user."""
        pages = {'/todos/new/': '/todos/sign_in/?next=/todos/new/',
                 '/todos/current/': '/todos/sign_in/?next=/todos/current/',
                 '/todos/completed/': '/todos/sign_in/?next=/todos/completed/',
                 f'/todos/{self.todo.id}/':
                     f'/todos/sign_in/?next=/todos/{self.todo.id}/',
                 f'/todos/{self.todo.id}/edit/':
                     f'/todos/sign_in/?next=/todos/{self.todo.id}/edit/',
                 '/todos/sign_out/': '/todos/sign_in/?next=/todos/sign_out/'}
        for page, value in pages.items():
            with self.subTest(page=page, value=value):
                response = self.guest_client.get(page)
                error_message = f'Error: no access to page {page}'
                self.assertRedirects(response, value, msg_prefix=error_message)

    def test_urls_authorized_client(self):
        """Access authorized user."""
        pages = ('/todos/new/',
                 '/todos/current/',
                 '/todos/completed/',
                 f'/todos/{self.todo.id}/',
                 f'/todos/{self.todo.id}/edit/',
                 '/todos/sign_up/',
                 '/todos/sign_in/')
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                error_message = f'Error: no access to page {page}'
                self.assertEqual(200, response.status_code, error_message)

    def test_urls_redirects_authorized_client(self):
        """Redirects authorized user."""
        pages = {'/todos/': '/todos/current/',
                 '/todos/sign_out/': '/todos/'}
        for page, value in pages.items():
            with self.subTest(page=page, value=value):
                response = self.authorized_client.get(page)
                error_message = f'Error: no access to page {page}'
                self.assertRedirects(response, value, msg_prefix=error_message)

    def test_urls_correct_template(self):
        """Test that the URL is using the correct template."""
        templates_url_names = {
            '/todos/': 'todo/index.html',
            '/todos/current/': 'todo/view_todos.html',
            '/todos/completed/': 'todo/completed_todos.html',
            '/todos/new/': 'todo/input_todo.html',
            f'/todos/{self.todo.id}/': 'todo/view_todo.html',
            f'/todos/{self.todo.id}/edit/': 'todo/input_todo.html',
            '/todos/sign_in/': 'todo/sign_in.html',
            '/todos/sign_up/': 'todo/sign_up.html',
        }
        for page, template in templates_url_names.items():
            with self.subTest(page=page):
                if page == '/todos/':
                    response = self.guest_client.get(page)
                else:
                    response = self.authorized_client.get(page)
                error_message = f'Error: {page} expected template {template}'
                self.assertTemplateUsed(response, template, error_message)
