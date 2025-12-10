from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core import mail
from django.conf import settings
from ..models import Category, LostItem, FoundItem, SuccessStory


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', DEFAULT_FROM_EMAIL='noreply@example.com')
class ClaimFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Phones')
        self.lost = LostItem.objects.create(
            title='Test Lost', category=self.cat, reporter_name='Alice', reporter_email='alice@example.com'
        )
        self.found = FoundItem.objects.create(
            title='Test Found', category=self.cat, finder_name='Bob', finder_email='bob@example.com'
        )

    def test_mark_lost_claim_creates_successstory_and_sends_email(self):
        url = reverse('mark_lost_claim', args=[self.lost.pk])
        resp = self.client.post(url, follow=True)
        self.lost.refresh_from_db()
        self.assertEqual(self.lost.status, 'claimed')
        self.assertTrue(SuccessStory.objects.filter(title__contains='Reunited').exists())
        # email sent to reporter
        self.assertEqual(len(mail.outbox), 1)

    def test_mark_found_claim_creates_successstory_and_sends_email(self):
        url = reverse('mark_found_claim', args=[self.found.pk])
        resp = self.client.post(url, follow=True)
        self.found.refresh_from_db()
        self.assertEqual(self.found.status, 'claimed')
        self.assertTrue(SuccessStory.objects.filter(title__contains='Found item claimed').exists())
        self.assertEqual(len(mail.outbox), 1)
