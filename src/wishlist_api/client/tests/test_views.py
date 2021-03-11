from unittest import mock

import pytest
from django.http import QueryDict
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.backends import UserModel
from oauth2_provider.models import AccessToken, Application
from rest_framework import status

from wishlist_api.client.views import (
    ClientListCreateView,
    ClientRetrieveUpdateDestroyView,
    logger
)


@pytest.mark.django_db
class TestClientViews:

    @pytest.fixture
    def mock_logger_info(self):
        with mock.patch.object(logger, 'info') as mock_logger_info:
            yield mock_logger_info

    @pytest.fixture
    def mock_logger_warning(self):
        with mock.patch.object(logger, 'warning') as mock_logger_warning:
            yield mock_logger_warning

    @pytest.fixture
    def setup_authentication(self):
        self.test_user = UserModel.objects.create_user(
            username='test_user',
            email='test@user.com',
            password='123456'
        )

        self.application = Application(
            name='Test Application',
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE
        )
        self.application.save()

        expired_at = timezone.now() + timezone.timedelta(days=1)

        self.access_token = AccessToken.objects.create(
            user=self.test_user,
            token='1234567890',
            application=self.application,
            scope='read write',
            expires=expired_at
        )

        self.auth = "Bearer {0}".format(self.access_token.token)

    def test_should_return_one_page_of_clients_when_numbers_of_clients_smaller_then_ten(  # noqa
        self,
        rf,
        setup_authentication,
        add_three_clients
    ):
        request = rf.get('/api/client/', HTTP_AUTHORIZATION=self.auth)
        response = ClientListCreateView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['links']['next'] is None
        assert response.data['total'] == 3
        assert response.data['page'] == 1

    def test_should_return_one_page_of_clients_when_numbers_of_clients_is_zero(
        self,
        rf,
        setup_authentication
    ):
        request = rf.get('/api/client/', HTTP_AUTHORIZATION=self.auth)
        response = ClientListCreateView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['links']['next'] is None
        assert response.data['total'] == 0
        assert response.data['page'] == 1

    def test_should_return_two_pages_of_clients_when_numbers_of_clients_more_then_ten(  # noqa
        self,
        rf,
        setup_authentication,
        add_more_then_ten_clients
    ):
        request = rf.get('/api/client/', HTTP_AUTHORIZATION=self.auth)
        response = ClientListCreateView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['links']['next'] == (
            'http://testserver/api/client/?page=2'
        )
        assert response.data['total'] == 11
        assert response.data['page'] == 1

    def test_should_return_empty_results_when_pagination_not_have_page(
        self,
        rf,
        setup_authentication,
        mock_paginate_queryset
    ):
        request = rf.get('/api/client/', HTTP_AUTHORIZATION=self.auth)
        response = ClientListCreateView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_should_return_client_when_client_is_created_with_success(
        self,
        rf,
        setup_authentication,
        mock_logger_info
    ):
        body = {'name': 'Marcela', 'email': 'marcela@test.com'}
        body_qd = QueryDict('', mutable=True)
        body_qd.update(body)

        request = rf.post(
            '/api/client/',
            data=body,
            HTTP_AUTHORIZATION=self.auth
        )
        response = ClientListCreateView.as_view()(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == body['name']
        assert response.data['email'] == body['email']
        mock_logger_info.assert_called_with(
            'Client created with success',
            client=body_qd
        )

    def test_should_return_error_404_when_body_is_invalid(
        self,
        rf,
        setup_authentication,
        mock_logger_warning
    ):
        body = {'name': 'Marcela'}
        body_qd = QueryDict('', mutable=True)
        body_qd.update(body)

        request = rf.post(
            '/api/client/',
            data=body,
            HTTP_AUTHORIZATION=self.auth
        )
        response = ClientListCreateView.as_view()(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock_logger_warning.assert_called_with(
            'Fail to created client',
            client=body_qd
        )

    def test_should_return_client_when_client_is_found(
        self,
        rf,
        setup_authentication,
        add_one_client
    ):
        kwargs = {'pk': '1'}
        url = reverse('client-retrieve-update-destroy', kwargs=kwargs)

        request = rf.get(url, HTTP_AUTHORIZATION=self.auth)
        response = ClientRetrieveUpdateDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Kevin'
        assert response.data['email'] == 'kevin@test.com'

    def test_should_return_error_404_when_client_not_found(
        self,
        rf,
        setup_authentication,
        add_one_client
    ):
        kwargs = {'pk': '2'}
        url = reverse('client-retrieve-update-destroy', kwargs=kwargs)

        request = rf.get(url, HTTP_AUTHORIZATION=self.auth)
        response = ClientRetrieveUpdateDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_return_client_when_update_client_with_success(
        self,
        rf,
        setup_authentication,
        add_one_client
    ):
        kwargs = {'pk': '1'}
        body = {'name': 'Kevin Souza', 'email': 'kevin@test.com'}
        url = reverse('client-retrieve-update-destroy', kwargs=kwargs)

        request = rf.put(
            url,
            data=body,
            HTTP_AUTHORIZATION=self.auth,
            content_type='application/json'
        )
        response = ClientRetrieveUpdateDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data['name'] == 'Kevin Souza'
        assert response.data['email'] == 'kevin@test.com'

    def test_should_return_error_404_when_not_found_client_to_update(
        self,
        rf,
        setup_authentication,
        add_one_client
    ):
        kwargs = {'pk': '2'}
        body = {'name': 'Kevin Souza', 'email': 'kevin@test.com'}
        url = reverse('client-retrieve-update-destroy', kwargs=kwargs)

        request = rf.put(
            url,
            data=body,
            HTTP_AUTHORIZATION=self.auth,
            content_type='application/json'
        )
        response = ClientRetrieveUpdateDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_return_client_when_partial_update_client_with_success(
        self,
        rf,
        setup_authentication,
        add_one_client
    ):
        kwargs = {'pk': '1'}
        body = {'name': 'Kevin Souza'}
        url = reverse('client-retrieve-update-destroy', kwargs=kwargs)

        request = rf.patch(
            url,
            data=body,
            HTTP_AUTHORIZATION=self.auth,
            content_type='application/json'
        )
        response = ClientRetrieveUpdateDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data['name'] == 'Kevin Souza'

    def test_should_return_error_404_when_not_found_client_to_partial_update(
        self,
        rf,
        setup_authentication,
        add_one_client
    ):
        kwargs = {'pk': '2'}
        body = {'name': 'Kevin Souza'}
        url = reverse('client-retrieve-update-destroy', kwargs=kwargs)

        request = rf.patch(
            url,
            data=body,
            HTTP_AUTHORIZATION=self.auth,
            content_type='application/json'
        )
        response = ClientRetrieveUpdateDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_delete_client_with_success(
        self,
        rf,
        setup_authentication,
        add_one_client
    ):
        kwargs = {'pk': '1'}
        url = reverse('client-retrieve-update-destroy', kwargs=kwargs)

        request = rf.delete(
            url,
            HTTP_AUTHORIZATION=self.auth,
            content_type='application/json'
        )
        response = ClientRetrieveUpdateDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_error_404_when_client_not_found(
        self,
        rf,
        setup_authentication,
        add_one_client
    ):
        kwargs = {'pk': '2'}
        url = reverse('client-retrieve-update-destroy', kwargs=kwargs)

        request = rf.delete(
            url,
            HTTP_AUTHORIZATION=self.auth,
            content_type='application/json'
        )
        response = ClientRetrieveUpdateDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_404_NOT_FOUND
