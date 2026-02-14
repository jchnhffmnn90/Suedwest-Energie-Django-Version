from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from unittest.mock import patch
import subprocess
from .forms import ContactForm
from .views import get_git_revision_hash

class UtilityTests(TestCase):
    @patch('subprocess.check_output')
    def test_git_revision_hash_success(self, mock_check_output):
        mock_check_output.return_value = b'abcdef123456\n'
        revision = get_git_revision_hash()
        self.assertEqual(revision, 'abcdef123456')

    @patch('subprocess.check_output')
    def test_git_revision_hash_failure(self, mock_check_output):
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'git')
        revision = get_git_revision_hash()
        self.assertEqual(revision, 'N/A')

    @patch('subprocess.check_output')
    def test_git_revision_hash_no_git(self, mock_check_output):
        mock_check_output.side_effect = FileNotFoundError
        revision = get_git_revision_hash()
        self.assertEqual(revision, 'N/A')


class PageViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Südwest Energie')

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_services_page(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services.html')

    def test_process_page(self):
        response = self.client.get(reverse('process'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'process.html')

    def test_imprint_page(self):
        response = self.client.get(reverse('imprint'))
        self.assertEqual(response.status_code, 200)
        # Assuming imprint renders home.html as placeholder or its own template if created
        # Based on views.py content it renders home.html
        self.assertTemplateUsed(response, 'home.html') 

    def test_privacy_page(self):
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_terms_page(self):
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_health_check(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'status': 'ok'})


class ContactPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')

    def test_contact_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_form_valid_submission(self):
        data = {
            'name': 'Test Firma GmbH',
            'contact_person': 'Max Mustermann',
            'email': 'test@example.com',
            'phone': '0123456789',
            'message': 'Dies ist eine Testnachricht.'
        }
        # Use follow=True to handle redirect and get messages in one go
        response = self.client.post(self.url, data, follow=True)
        
        self.assertRedirects(response, self.url)
        
        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Neue Anfrage von Test Firma GmbH')
        self.assertIn('Dies ist eine Testnachricht.', mail.outbox[0].body)
        
        # Check for success message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns umgehend bei Ihnen.')

    def test_contact_form_invalid_submission(self):
        # Missing required fields (email and message)
        data = {
            'name': 'Test Firma GmbH',
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 200)
        
        # Manual form error checking (more robust than assertFormError sometimes)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('message', form.errors)
        self.assertEqual(form.errors['email'], ['Dieses Feld ist zwingend erforderlich.'])
        
        # No email should be sent
        self.assertEqual(len(mail.outbox), 0)


class StatusPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('status')
        self.user = User.objects.create_user(username='user', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')

    def test_status_page_anonymous(self):
        # Redirect to login
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/admin/login/?next={self.url}')

    def test_status_page_regular_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get(self.url)
        # Expect redirect to login (default behavior of user_passes_test if not logged in or fails test)
        # Wait, user_passes_test redirects to login_url if test fails.
        self.assertRedirects(response, f'/admin/login/?next={self.url}')

    def test_status_page_superuser(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status.html')
        self.assertContains(response, 'System Status')
        self.assertContains(response, 'Datenbank')
