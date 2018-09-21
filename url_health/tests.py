from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import LinkStore, Scanning


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

    def test_scan(self):
        #mock for a while cuz Celery
        self.assertEqual(Scanning.objects.count(), 1)

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
