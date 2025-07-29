from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        res = self.client.get('/')
        self.assertTemplateUsed(res, 'home.html')

    def test_renders_input_form(self):
        res = self.client.get('/')
        self.assertContains(res, '<form method="POST">')
        self.assertContains(res, '<input name="item_text"')

    def test_can_make_post_request(self):
        res = self.client.post('/', data={"item_text": "A new list item"})
        self.assertContains(res, "A new list item")
        self.assertTemplateUsed(res, 'home.html')


class ItemModelTest(TestCase):
    def test_saving_retrieving_items(self):
        first_item = Item()
        first_item.text = "The very first item"
        first_item.save()

        second_item = Item()
        second_item.text = "The second"
        second_item.save()

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)

        first = items[0]
        second = items[1]

        self.assertEqual("The very first item", first.text)
        self.assertEqual("The second", second.text)
