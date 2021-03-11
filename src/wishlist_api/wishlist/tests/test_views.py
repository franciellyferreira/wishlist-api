from unittest import mock

import pytest
from django.http import QueryDict
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.backends import UserModel
from oauth2_provider.models import AccessToken, Application
from rest_framework import status

from wishlist_api.wishlist.views import (
    WishlistCreateView,
    WishlistDestroyView,
    WishlistListView,
    logger
)


@pytest.mark.django_db
class TestWishlistViews:

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

    def test_should_return_item_wishlist_when_add_product_with_success(
        self,
        rf,
        setup_authentication,
        product_id,
        client,
        mock_logger_info
    ):
        body = {'client': '1', 'product_id': str(product_id)}
        body_qd = QueryDict('', mutable=True)
        body_qd.update(body)

        request = rf.post(
            '/api/wishlist/',
            data=body,
            HTTP_AUTHORIZATION=self.auth
        )
        response = WishlistCreateView.as_view()(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['client'] == int(body['client'])
        assert response.data['product_id'] == str(body['product_id'])
        mock_logger_info.assert_called_with(
            'Product added in wishlist',
            data=body_qd
        )

    def test_should_return_error_400_when_client_not_exists(
        self,
        rf,
        setup_authentication,
        product_id,
        client,
        mock_logger_warning
    ):
        body = {'client': '2', 'product_id': str(product_id)}
        body_qd = QueryDict('', mutable=True)
        body_qd.update(body)

        request = rf.post(
            '/api/wishlist/',
            data=body,
            HTTP_AUTHORIZATION=self.auth
        )
        response = WishlistCreateView.as_view()(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock_logger_warning.assert_called_with(
            'Fail added product in wishlist',
            data=body_qd
        )

    def test_should_return_error_404_when_product_not_found(
        self,
        rf,
        setup_authentication,
        product_id_not_exists,
        client
    ):
        body = {'client': '1', 'product_id': str(product_id_not_exists)}
        body_qd = QueryDict('', mutable=True)
        body_qd.update(body)

        request = rf.post(
            '/api/wishlist/',
            data=body,
            HTTP_AUTHORIZATION=self.auth
        )
        response = WishlistCreateView.as_view()(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'product_id': 'Not found in Magalu'}

    def test_should_return_error_404_when_client_already_exists_in_wishlist(
        self,
        rf,
        setup_authentication,
        add_one_wishlist,
        product_id,
        client
    ):
        body = {'client': '1', 'product_id': str(product_id)}
        body_qd = QueryDict('', mutable=True)
        body_qd.update(body)

        request = rf.post(
            '/api/wishlist/',
            data=body,
            HTTP_AUTHORIZATION=self.auth
        )
        response = WishlistCreateView.as_view()(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'product_id': 'Already exists in wishlist'}

    def test_should_return_list_of_clients_when_wishlist_by_client_exists(
        self,
        rf,
        setup_authentication,
        add_multi_products_wishlist
    ):
        kwargs = {'pk': 1}
        url = reverse('wishlist-list', kwargs=kwargs)

        request = rf.get(url, HTTP_AUTHORIZATION=self.auth)
        response = WishlistListView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['links']['next'] is None
        assert response.data['total'] == 3
        assert response.data['page'] == 1

    def test_should_return_error_404_when_client_not_found(
        self,
        rf,
        setup_authentication,
        add_multi_products_wishlist
    ):
        kwargs = {'pk': 100}
        url = reverse('wishlist-list', kwargs=kwargs)

        request = rf.get(url, HTTP_AUTHORIZATION=self.auth)
        response = WishlistListView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'client_id': 'Client not found'}

    def test_should_return_error_404_when_wishlist_not_found(
        self,
        rf,
        setup_authentication,
        client
    ):
        kwargs = {'pk': 1}
        url = reverse('wishlist-list', kwargs=kwargs)

        request = rf.get(url, HTTP_AUTHORIZATION=self.auth)
        response = WishlistListView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'client_id': 'Wishlist not found.'}

    def test_should_delete_product_of_wishlist_with_success(
        self,
        rf,
        setup_authentication,
        add_one_wishlist,
        product_id
    ):
        kwargs = {'pk': '1', 'product': str(product_id)}
        url = reverse('wishlist-destroy', kwargs=kwargs)

        request = rf.delete(
            url,
            HTTP_AUTHORIZATION=self.auth,
            content_type='application/json'
        )
        response = WishlistDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_return_success_when_client_and_product_not_exists(
        self,
        rf,
        setup_authentication,
        add_one_wishlist,
        product_id_not_exists
    ):
        kwargs = {'pk': '2', 'product': str(product_id_not_exists)}
        url = reverse('wishlist-destroy', kwargs=kwargs)

        request = rf.delete(
            url,
            HTTP_AUTHORIZATION=self.auth,
            content_type='application/json'
        )
        response = WishlistDestroyView.as_view()(request, **kwargs)

        assert response.status_code == status.HTTP_204_NO_CONTENT
