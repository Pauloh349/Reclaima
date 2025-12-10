from django.test import TestCase, override_settings, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from ..models import Category, LostItem, FoundItem, SuccessStory
import io


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', DEFAULT_FROM_EMAIL='noreply@example.com')
class ReportAndProofTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='TestCat')

    def test_report_lost_with_image_creates_item_and_thumbnail(self):
        img = SimpleUploadedFile('test.png', b'\x89PNG\r\n\x1a\n' + b'0' * 1024, content_type='image/png')
        url = reverse('report_lost')
        data = {
            'title': 'Lost Phone',
            'category': self.cat.pk,
            'description': 'My phone is missing',
            'location': 'Park',
            'date_lost': '2025-12-01',
            'reporter_name': 'Alice',
            'reporter_email': 'alice@example.com',
        }
        response = self.client.post(url, data={**data, 'image': img}, follow=True)
        self.assertEqual(LostItem.objects.filter(title='Lost Phone').count(), 1)
        item = LostItem.objects.get(title='Lost Phone')
        self.assertTrue(item.image.name)

    def test_claim_with_proof_creates_successstory_and_sends_email(self):
        item = LostItem.objects.create(title='Claimable', category=self.cat, reporter_name='Bob', reporter_email='bob@example.com')
        url = reverse('mark_lost_claim', args=[item.pk])
        response = self.client.post(url, data={'proof': 'I have photo of pickup'}, follow=True)
        item.refresh_from_db()
        self.assertEqual(item.status, 'claimed')
        self.assertTrue(SuccessStory.objects.filter(title__icontains='Reunited').exists())
        # an email should have been sent
        self.assertEqual(len(mail.outbox), 1)
