from __future__ import absolute_import, unicode_literals

from allauth.account.views import password_change
from allauth.socialaccount.views import connections
from django.conf import settings
from django.contrib.auth import authenticate
from django.test import TestCase
from faker import Factory

from xSACdb.test_helpers import BaseTest, ViewTestMixin
from xsd_auth.models import User
from xsd_members.models import MemberProfile


class UserTest(TestCase):
    fake = Factory.create(settings.FAKER_LOCALE)
    fake.seed(settings.RANDOM_SEED)
    FIRST_NAME = fake.first_name()
    LAST_NAME = fake.last_name()
    EMAIL = fake.email()
    PASSWORD = fake.password()

    def create_user(self):
        user = User.objects.create_user(
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            email=self.EMAIL,
            password=self.PASSWORD
        )
        user.save()
        return user

    def test_create_user(self):
        user = self.create_user()
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, self.FIRST_NAME)
        self.assertEqual(user.last_name, self.LAST_NAME)
        self.assertEqual(user.email, self.EMAIL)
        self.assertTrue(len(user.password) > 0)

    def test_username_authentication(self):
        user_a = self.create_user()
        user_b = authenticate(
            username=user_a.username,
            password=self.PASSWORD,
        )
        self.assertEqual(user_a, user_b)

    def test_email_authentication(self):
        user_a = self.create_user()
        user_b = authenticate(
            username=self.EMAIL,
            password=self.PASSWORD,
        )
        self.assertEqual(user_a, user_b)

    def test_full_name(self):
        user = self.create_user()
        self.assertEqual(user.get_full_name(), u"{0} {1}".format(
            self.FIRST_NAME, self.LAST_NAME
        ))

    def test_get_short_name(self):
        user = self.create_user()
        self.assertEqual(user.get_short_name(), self.FIRST_NAME)

    def test_first_name(self):
        user = self.create_user()
        self.assertEqual(user.get_first_name(), self.FIRST_NAME)

    def test_last_name(self):
        user = self.create_user()
        self.assertEqual(user.get_last_name(), self.LAST_NAME)

    def test_email_user(self):
        user = self.create_user()
        user.email_user('subject', 'message', 'from@example.com')

    def test_get_profile(self):
        user = self.create_user()
        self.assertIsInstance(user.get_profile(), MemberProfile)

    def test_profile_image_url(self):
        user = self.create_user()
        self.assertIsInstance(user.profile_image_url(), basestring)

    def test_unicode(self):
        user = self.create_user()
        self.assertEqual(unicode(user), user.get_full_name())


class PasswordChangeViewTest(ViewTestMixin, BaseTest):
    view = password_change
    url_name = 'xsd_auth:account_change_password'
    template_name = 'account/password_change.html'
    allowed_unverified = True

    # TODO test password change


class SocialAccountConnectionsViewTest(ViewTestMixin, BaseTest):
    view = connections
    url_name = 'xsd_auth:socialaccount_connections'
    template_name = 'socialaccount/connections.html'
    allowed_unverified = True