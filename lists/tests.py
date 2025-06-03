from django.test import TestCase

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

