from django.test import TestCase

from todo.forms import TodoCreateForm


class TestTodoCreateForm(TestCase):
    """Tests for TodoCreateForm"""

    def test_form_has_title_and_description_fields(self):
        form = TodoCreateForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)

    def test_create_valid_form_data(self):
        form = TodoCreateForm(data={
            'title': 'valid title',
            'description': 'valid description'
        })
        self.assertTrue(form.is_valid())

    def test_create_invalid_form_data(self):
        form = TodoCreateForm(data={
            'title': 'A' * 1000,
            'description': 'valid description' * 1000
        })
        self.assertFalse(form.is_valid())

