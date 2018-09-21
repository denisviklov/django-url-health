import subprocess
from unittest.mock import patch, Mock

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import LinkStore, Scanning, TokenStore
from .tasks import scan_links

class ViewsTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.enforce_csrf_checks = True
        self.client.login(username='temporary', password='temporary')
        Scanning.objects.create()

    def test_index_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_post(self):
        response = self.client.post(
                reverse('index'),
                {'link': 'https://test.com', 'description': 'test'}
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LinkStore.objects.count(), 1)

    @patch('url_health.views.scan_links.delay')
    def test_scan(self, mocked_delay):
        response = self.client.get(reverse('scan'))
        self.assertEqual(response.status_code, 302)

    @patch('url_health.views.scan_links.delay')
    def test_scan_first_time(self, mocked_delay):
        Scanning.objects.all().delete()
        response = self.client.get(reverse('scan'))
        self.assertEqual(response.status_code, 302)

    @patch('url_health.views.scan_links.delay')
    def test_scan_already_run(self, mocked_delay):
        scan = Scanning.objects.first()
        scan.status = Scanning.RUN
        scan.save()
        response = self.client.get(reverse('scan'))
        self.assertEqual(response.status_code, 302)

    def test_poll_results(self):
        response = self.client.get(reverse('poll_results'))
        self.assertEqual(response.status_code, 200)

    def test_link_delete(self):
        link = LinkStore.objects.create(link='https://test.com')
        response = self.client.get(reverse('delete_url', kwargs={'id': link.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LinkStore.objects.count(), 0)

    def test_scan_results(self):
        response = self.client.get(reverse('scan_results'))
        self.assertEqual(response.status_code, 200)

    def test_fetch_links(self):
        response = self.client.get(reverse('fetch_links'))
        self.assertEqual(response.status_code, 200)

    def test_post_link_info(self):
        link = LinkStore.objects.create(link='https://test.com')
        response = self.client.post(reverse('post_link_info'),
            {'link':'https://test.com', 'status': 200})
        self.assertEqual(response.status_code, 200)
        link = LinkStore.objects.first()
        self.assertEqual(link.status, 200)

    def test_post_link_info_wrong_url(self):
        LinkStore.objects.create(link='https://test.com')
        response = self.client.post(reverse('post_link_info'),
            {'link': 'test.com'})
        self.assertEqual(response.status_code, 404)

    def test_post_link_info_wrong_form(self):
        LinkStore.objects.create(link='test.com')
        response = self.client.post(reverse('post_link_info'),
            {'link': 'test.com', 'status': '200'})
        self.assertEqual(response.status_code, 200)

    def test_stop_scan(self):
        scan = Scanning.objects.first()
        scan.status = 1
        scan.save()
        response = self.client.get(reverse('poll_results'))
        self.assertEqual(response.status_code, 200)

    def test_task(self):

        with patch.object(subprocess, 'check_call', return_value=None) as mock_method:
            scan_links('https://tester.com')

    def test_task_fail(self):
        from url_health.tasks import scan_links
        import subprocess
        def raise_(ex):
            raise ex
        with patch.object(subprocess, 'check_call', return_value=lambda: raise_(Exception('foobar'))) as mock_method:
            mock_method.raiseError.side_effect = Mock(side_effect=Exception('Test'))
            scan_links('https://tester.com')

    def test_token(self):
        TokenStore.objects.create()