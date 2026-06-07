from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserPermissionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin@example.com", "Passw0rd!", full_name="Admin", role=User.Role.ADMIN, is_staff=True)
        self.manager = User.objects.create_user("manager@example.com", "Passw0rd!", full_name="Manager", role=User.Role.MANAGER)

    def test_admin_can_access_user_management(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)

    def test_manager_is_redirected_from_user_management(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse("user_list"))
        self.assertRedirects(response, reverse("dashboard"))
