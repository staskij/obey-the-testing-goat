from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_post_req(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["item_text"] = 'A new list item'
        response = home_page(request)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_only_saves_items_when_not_empty(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        text1 = 'The first (ever) list item'
        first_item.text = text1
        first_item.save()
        second_item = Item()
        text2 = 'Item the second '
        second_item.text = text2
        second_item.save()
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, text1)
        self.assertEqual(second_saved_item.text, text2)