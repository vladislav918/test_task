from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect

from .models import Memory, CustomUser, Coordinates


class TestMemoryListView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = CustomUser.objects.create_user(username='testuser', password='12345')
        self.user2 = CustomUser.objects.create_user(username='anotheruser', password='67890')

        self.coordinate = Coordinates.objects.create(lat=40.7128, lng=-74.0060)

        self.memory1 = Memory.objects.create(
            title='Воспоминание 1',
            comment='Плохое',
            coordinates=self.coordinate,
            author=self.user1
        )
        self.memory2 = Memory.objects.create(
            title='Воспоминание 2',
            comment='Хорошее',
            coordinates=self.coordinate,
            author=self.user1
        )

    def test_memory_list_view_for_logged_in_user(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse('memory_list'))
        self.assertEqual(response.status_code, 200)

        memory_titles = [memory.title for memory in response.context['object_list']]
        self.assertEqual(memory_titles, [self.memory2.title, self.memory1.title])

    def test_memory_list_view_for_anonymous_user(self):
        response = self.client.get(reverse('memory_list'))
        self.assertEqual(response.status_code, 302)

    def test_login_url(self):
        self.assertEqual(settings.LOGIN_URL, 'home')

    def test_template_used(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('memory_list'))
        self.assertTemplateUsed(response, 'places_remember/memory_list.html')


class TestMemoryAddView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create_user(username='testuser', password='12345')

    def test_memory_list_view_for_anonymous_user(self):
        response = self.client.get(reverse('add_memory'))
        self.assertEqual(response.status_code, 302)

    def test_memory_add_view_post_success(self):
        self.client.force_login(self.user)

        form_data = {
            'title': 'Воспоминание 1',
            'comment': 'Комментарий',
            'latitude': 40.7128,
            'longitude': -74.0060,
        }

        response = self.client.post(reverse_lazy('add_memory'), data=form_data)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, reverse_lazy('memory_list'))

        self.assertTrue(Memory.objects.exists())

        created_memory = Memory.objects.first()

        self.assertEqual(created_memory.title, form_data['title'])
        self.assertEqual(created_memory.comment, form_data['comment'])

        self.assertTrue(Coordinates.objects.exists())

        created_coordinates = Coordinates.objects.first()

        self.assertEqual(created_coordinates.lat, form_data['latitude'])
        self.assertEqual(created_coordinates.lng, form_data['longitude'])
        self.assertEqual(created_memory.coordinates, created_coordinates)

    def test_template_used(self):
        self.client.force_login(self.user)

        self.coordinate = Coordinates.objects.create(lat=40.7128, lng=-74.0060)

        self.memory = Memory.objects.create(
            title='Воспоминание 1',
            comment='Плохое',
            coordinates=self.coordinate,
            author=self.user
        )

        response = self.client.get(reverse('update_page', kwargs={'pk': self.memory.id}))
        self.assertTemplateUsed(response, 'places_remember/memory_update_form.html')
