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

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self):
        res = self.client.post('/', data={"item_text": "A new list item"})
        self.assertRedirects(res, "/")


    def test_only_things_when_necessary(self):
        res = self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text="Itemey 1")
        Item.objects.create(text="Itemey 2")

        res = self.client.get("/")

        self.assertContains(res, "Itemey 1")
        self.assertContains(res, "Itemey 2")

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
