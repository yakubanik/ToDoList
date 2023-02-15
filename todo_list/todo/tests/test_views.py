from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import ObjectDoesNotExist

from todo.models import Todo

User = get_user_model()


class TodoViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='User1')
        self.user2 = User.objects.create_user(username='User2',
                                              password='12345')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.todo = Todo.objects.create(title='Test title',
                                        description='Test description',
                                        author=self.user)

    def test_views_correct_template(self):
        """Checking that the URL is using the correct template"""
        templates_url_names = {
            reverse('index'): 'todo/index.html',
            reverse('current_todos'): 'todo/view_todos.html',
            reverse('completed_todos'): 'todo/completed_todos.html',
            reverse('create_todo'): 'todo/input_todo.html',
            reverse('view_todo', kwargs={'todo_id': self.todo.id}):
                'todo/view_todo.html',
            reverse('edit_todo', kwargs={'todo_id': self.todo.id}):
                'todo/input_todo.html',
            reverse('sign_in'): 'todo/sign_in.html',
            reverse('sign_up'): 'todo/sign_up.html',
        }

        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                if address == reverse('index'):
                    response = self.guest_client.get(address)
                else:
                    response = self.authorized_client.get(address)
                error_message = f'Error: {address} expected template {template}'
                self.assertTemplateUsed(response, template, error_message)

    def test_view_todo_page_show_correct_context(self):
        """Page view_todo formed with correct context."""
        response = self.authorized_client.get(
            reverse('view_todo', kwargs={'todo_id': self.todo.id}))
        self.assertEqual(self.todo.title, response.context.get('todo').title)
        self.assertEqual(self.todo.description,
                         response.context.get('todo').description)
        self.assertEqual(self.todo.id, response.context.get('todo').id)

    def test_current_todos_page_show_correct_context(self):
        """Page current_todos formed with correct context."""
        response = self.authorized_client.get(reverse('current_todos'))
        first_object = response.context['todos'][0]
        self.assertEqual(self.todo.title, first_object.title)
        self.assertEqual(self.todo.description, first_object.description)
        self.assertEqual(self.todo.id, first_object.id)

    def test_create_todo_with_valid_data(self):
        """Test creating todo with correct data."""
        response = self.authorized_client.post(reverse('create_todo'),
                                               {'title': 'test title',
                                                'description': 'some text'})
        self.assertRedirects(response, reverse('current_todos'))

    def test_create_todo_with_invalid_data(self):
        """Test creating todo with too long title."""
        response = self.authorized_client.post(reverse('create_todo'),
                                               {'title': 'A' * 200,
                                                'description': 'some text'})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Bad data passed in. Try again.")

    def test_edit_todo_with_valid_data(self):
        """Test editing todo with correct data."""
        response = self.authorized_client.post(
            reverse('edit_todo', kwargs={'todo_id': self.todo.id}),
            {'title': 'Changed title',
             'description': 'Changed text'})
        edited_todo = Todo.objects.get(pk=self.todo.id)
        self.assertEqual('Changed title', edited_todo.title)
        self.assertEqual('Changed text', edited_todo.description)
        self.assertRedirects(response, reverse('current_todos'))

    def test_edit_todo_with_invalid_data(self):
        """Test editing todo with too long title."""
        response = self.authorized_client.post(
            reverse('edit_todo', kwargs={'todo_id': self.todo.id}),
            {'title': 'A' * 200,
             'description': 'Changed text'})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Bad data passed in. Try again.")
        self.assertNotEqual(self.todo.title, 'A' * 200)
        self.assertNotEqual(self.todo.description, 'Changed text')

    def test_complete_existing_todo(self):
        """Test complete todo."""
        response = self.authorized_client.post(
            reverse('complete_todo', kwargs={'todo_id': self.todo.id}))
        completed_todo = Todo.objects.get(pk=self.todo.id)
        self.assertTrue(completed_todo.completed)
        self.assertRedirects(response, reverse('current_todos'))

    def test_complete_non_existing_todo(self):
        """Test complete todo that not exist."""
        response = self.authorized_client.post(
            reverse('complete_todo', kwargs={'todo_id': self.todo.id + 1}))
        self.assertEqual(404, response.status_code)

    def test_delete_todo(self):
        """Test deleting todo."""
        self.authorized_client.post(
            reverse('delete_todo', kwargs={'todo_id': self.todo.id}))
        with self.assertRaises(ObjectDoesNotExist):
            Todo.objects.get(pk=self.todo.id)

    def test_sign_up_with_valid_data(self):
        """Test sign up with correct data."""
        response = self.guest_client.post(reverse('sign_up'),
                                          {'username': 'New_user',
                                           'password1': 'password',
                                           'password2': 'password'})
        self.assertRedirects(response, reverse('current_todos'))

    def test_sign_up_with_mismatched_passwords(self):
        """Test sign up with passwords that do not match."""
        response = self.guest_client.post(reverse('sign_up'),
                                          {'username': 'New_user',
                                           'password1': 'password',
                                           'password2': 'password2'})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Passwords do not match')

    def test_sign_up_with_taken_login(self):
        """Test sign up with already taken login."""
        response = self.guest_client.post(reverse('sign_up'),
                                          {'username': 'User1',
                                           'password1': 'password',
                                           'password2': 'password'})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Login is already taken')

    def test_sign_in_with_valid_data(self):
        """Test sign in with correct data."""
        response = self.guest_client.post(reverse('sign_in'),
                                          {'username': 'User2',
                                           'password': '12345'})
        self.assertRedirects(response, reverse('current_todos'))

    def test_sing_in_with_invalid_data(self):
        """Test sign in with invalid data."""
        response = self.guest_client.post(reverse('sign_in'),
                                          {'username': 'User123',
                                           'password': '12345'})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Incorrect username and/or password')

    def test_todo_created_correctly_user2(self):
        """Test that todos after creating not add to other users."""
        todo = Todo.objects.create(title='title from user2',
                                   description='other description',
                                   author=self.user2)
        response = self.authorized_client.get(reverse('current_todos'))
        user1_todos = response.context['todos']
        self.assertNotIn(todo, user1_todos)

