"""API tests for listing document upload."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.documents.models import Document
from doion.identity.factories import ProfileFactory
from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def owner(db):
    user = UserFactory.create(password=get_random_string(12))
    ProfileFactory.create(user=user, role=user.role)
    return user


@pytest.fixture
def other_user(db):
    user = UserFactory.create(password=get_random_string(12))
    ProfileFactory.create(user=user, role=user.role)
    return user


@pytest.fixture
def listing(db, owner):
    return ChequeListingFactory.create(
        owner=owner,
        issuer=IssuerProfileFactory.create(),
    )


@pytest.mark.django_db
class TestListingDocumentUpload:
    def test_owner_can_upload_cheque_image(self, api_client, owner, listing):
        api_client.force_authenticate(user=owner)
        upload = SimpleUploadedFile("cheque.jpg", b"fake-image", content_type="image/jpeg")

        response = api_client.post(
            f"/api/v1/listings/{listing.id}/documents/",
            {"document_type": Document.DocumentType.CHEQUE_IMAGE, "file": upload},
            format="multipart",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Document.objects.filter(
            owner=owner,
            related_object_type="cheque_listing",
            related_object_id=str(listing.id),
            document_type=Document.DocumentType.CHEQUE_IMAGE,
        ).exists()

    def test_non_owner_cannot_upload_document(self, api_client, other_user, listing):
        api_client.force_authenticate(user=other_user)
        upload = SimpleUploadedFile("cheque.jpg", b"fake-image", content_type="image/jpeg")

        response = api_client.post(
            f"/api/v1/listings/{listing.id}/documents/",
            {"document_type": Document.DocumentType.CHEQUE_IMAGE, "file": upload},
            format="multipart",
        )

        # Non-owner is filtered out of queryset -> 404, or explicit 403 if object reachable
        assert response.status_code in {403, 404}

    def test_upload_requires_authentication(self, api_client, listing):
        upload = SimpleUploadedFile("cheque.jpg", b"fake-image", content_type="image/jpeg")

        response = api_client.post(
            f"/api/v1/listings/{listing.id}/documents/",
            {"document_type": Document.DocumentType.CHEQUE_IMAGE, "file": upload},
            format="multipart",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_upload_rejects_invalid_document_type(self, api_client, owner, listing):
        api_client.force_authenticate(user=owner)
        upload = SimpleUploadedFile("cheque.jpg", b"fake-image", content_type="image/jpeg")

        response = api_client.post(
            f"/api/v1/listings/{listing.id}/documents/",
            {"document_type": "not_a_real_type", "file": upload},
            format="multipart",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
