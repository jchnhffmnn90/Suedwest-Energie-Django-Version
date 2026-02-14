from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from .models import Visit
import time

class MiddlewareIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_visit_logging_middleware(self):
        """Test that the VisitTrackingMiddleware correctly logs visits."""
        # Initial count
        initial_count = Visit.objects.count()
        
        # Visit home page
        response = self.client.get(reverse('home'), HTTP_USER_AGENT='TestAgent')
        self.assertEqual(response.status_code, 200)
        
        # Check if a visit was recorded
        self.assertEqual(Visit.objects.count(), initial_count + 1)
        visit = Visit.objects.latest('timestamp')
        self.assertEqual(visit.path, '/')
        self.assertEqual(visit.user_agent, 'TestAgent')
        # Client IP is 127.0.0.1 by default in tests, anonymized should be 127.0.0.0
        self.assertEqual(visit.ip_address_anonymized, '127.0.0.0')

    def test_excluded_paths_not_logged(self):
        """Test that excluded paths (health, admin, etc.) are not logged."""
        initial_count = Visit.objects.count()
        
        # Visit health check
        self.client.get(reverse('health_check'))
        # Visit admin (even if redirected)
        self.client.get('/admin/')
        # Visit a fake static file path (if we can simulate it)
        self.client.get('/static/test.css')
        
        # Count should still be the same
        self.assertEqual(Visit.objects.count(), initial_count)

    def test_ipv6_anonymization(self):
        """Test that IPv6 addresses are correctly anonymized by the middleware."""
        # We need to simulate an IPv6 REMOTE_ADDR
        # Note: Client doesn't easily allow setting REMOTE_ADDR in a way that bypasses middleware logic if not careful
        # but let's try with REMOTE_ADDR in extra
        self.client.get(reverse('home'), REMOTE_ADDR='2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        
        visit = Visit.objects.latest('timestamp')
        self.assertEqual(visit.ip_address_anonymized, '2001:0db8::XXXX')


class TemplateIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_common_elements_on_all_pages(self):
        """Verify that common UI elements are present on all major pages."""
        urls = [reverse('home'), reverse('about'), reverse('services'), reverse('process'), reverse('contact')]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Page {url} failed to load")
            
            # Check for Navbar Brand / Logo
            self.assertContains(response, 'Südwest Energie')
            self.assertContains(response, 'logo.png')
            
            # Check for Navigation Links
            self.assertContains(response, 'STARTSEITE')
            self.assertContains(response, 'ÜBER UNS')
            
            # Check for Footer Contact Info
            self.assertContains(response, 'Thomke & Thomke GbR')
            self.assertContains(response, 'kontakt@suedwest-energie.de')
            self.assertContains(response, '0176 / 134 27 945')


class WorkflowIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='password')

    def test_full_user_journey(self):
        """Simulate a user visiting the site and sending a contact request."""
        # 1. User arrives on home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # 2. User goes to 'About'
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        
        # 3. User goes to 'Contact'
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        
        # 4. User submits the form
        data = {
            'name': 'Integration Test Corp',
            'email': 'integration@test.com',
            'message': 'This is an integrated workflow test.'
        }
        response = self.client.post(reverse('contact'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vielen Dank!')
        
        # 5. Verify email integration
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Integration Test Corp', mail.outbox[0].subject)
        
        # 6. Verify visit logs integration
        # (Home, About, Contact GET, Contact POST, Redirect GET) = 5 visits
        self.assertEqual(Visit.objects.count(), 5)
        
        # 7. Admin checks the status page
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('status'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '5') # visits_total should be 5
        self.assertContains(response, '/ueber-uns/')
        self.assertContains(response, '/kontakt/')
