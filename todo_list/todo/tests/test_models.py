from django.test import TestCase
from django.contrib.auth.models import User

from todo.models import Todo


class TestTodo(TestCase):
    """Tests for Todo model"""

    @classmethod
    def setUpTestData(cls):
        cls.todo = Todo.objects.create(title="Test title",
                                       author=User.objects.create())

    def test_model_str(self):
        title = self.todo.title
        self.assertEqual(title, str(self.todo))

    def test_title_max_length(self):
        title_field = self.todo._meta.get_field('title')
        real_max_length = getattr(title_field, 'max_length')
        self.assertEqual(100, real_max_length)

    def test_absolute_url(self):
        url = self.todo.get_absolute_url()
        self.assertEqual('/todos/1/', url)
