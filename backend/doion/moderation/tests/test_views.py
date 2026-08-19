import pytest
from rest_framework.test import APIClient

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.users.factories import UserFactory


@pytest.fixture
def moderator(db):
    return UserFactory.create(as_moderator=True)


@pytest.fixture
def check_holder(db):
    return UserFactory.create()


@pytest.fixture
def issuer(db):
    return IssuerProfileFactory.create(
        national_or_company_id="1234567890",
        name="Test Issuer",
    )


@pytest.fixture
def pending_listing(db, check_holder, issuer):
    return ChequeListingFactory.create(
        pending=True,
        owner=check_holder,
        issuer=issuer,
        bank_name="بانک ملت",
        cheque_serial_number="1234567890123456",
        face_amount=500000000,
        due_date="2026-12-31",
        issuer_type="legal",
        issuer_name="شرکت فناوری نوین",
        issuer_national_id="1234567890",
    )


@pytest.fixture
def published_listing(db, check_holder, issuer):
    return ChequeListingFactory.create(
        published=True,
        owner=check_holder,
        issuer=issuer,
        bank_name="بانک ملت",
        cheque_serial_number="9999888877776666",
        face_amount=300000000,
        due_date="2026-12-31",
        issuer_type="natural",
        issuer_name="رضا کریمی",
        issuer_national_id="0012345678",
    )


@pytest.mark.django_db
class TestModerationQueueEndpoint:
    def test_queue_returns_only_pending(self, moderator, pending_listing, published_listing):
        client = APIClient()
        client.force_authenticate(user=moderator)

        response = client.get("/api/v1/moderation/queue/")

        assert response.status_code == 200
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert pending_listing.id in ids
        assert published_listing.id not in ids
        pending_item = next(item for item in results if item["id"] == pending_listing.id)
        assert pending_item["bank"]["code"] == "mellat"
        assert pending_item["bank_name"] == "بانک ملت"
        assert "aliases" not in pending_item["bank"]

    def test_queue_empty_when_no_pending(self, moderator, published_listing):
        client = APIClient()
        client.force_authenticate(user=moderator)

        response = client.get("/api/v1/moderation/queue/")

        assert response.status_code == 200
        results = response.data["results"] if "results" in response.data else response.data
        assert len(results) == 0

    def test_queue_requires_moderator_role(self, check_holder, pending_listing):
        client = APIClient()
        client.force_authenticate(user=check_holder)

        response = client.get("/api/v1/moderation/queue/")

        assert response.status_code == 403

    def test_queue_requires_authentication(self, pending_listing):
        client = APIClient()

        response = client.get("/api/v1/moderation/queue/")

        assert response.status_code == 401


@pytest.mark.django_db
class TestModerationDecisionEndpoint:
    def test_approve_listing(self, moderator, pending_listing):
        client = APIClient()
        client.force_authenticate(user=moderator)

        response = client.post(
            f"/api/v1/moderation/{pending_listing.id}/decision/",
            {"decision": "approve"},
        )

        assert response.status_code == 201
        assert response.data["decision"] == "approved"

        pending_listing.refresh_from_db()
        assert pending_listing.status == ChequeListing.Status.PUBLISHED

    def test_reject_listing(self, moderator, pending_listing):
        client = APIClient()
        client.force_authenticate(user=moderator)

        response = client.post(
            f"/api/v1/moderation/{pending_listing.id}/decision/",
            {
                "decision": "reject",
                "rejection_code": "MOD_101",
                "rejection_note": "اطلاعات ناقص",
            },
        )

        assert response.status_code == 201
        assert response.data["decision"] == "rejected"
        assert response.data["rejection_code"] == "MOD_101"

        pending_listing.refresh_from_db()
        assert pending_listing.status == ChequeListing.Status.REJECTED
        assert pending_listing.rejection_code == "MOD_101"
        assert pending_listing.resubmit_count == 1

    def test_reject_without_code_returns_400(self, moderator, pending_listing):
        client = APIClient()
        client.force_authenticate(user=moderator)

        response = client.post(
            f"/api/v1/moderation/{pending_listing.id}/decision/",
            {"decision": "reject"},
        )

        assert response.status_code == 400

    def test_reject_after_three_resubmits_returns_mod_306(self, moderator, pending_listing):
        pending_listing.resubmit_count = 3
        pending_listing.save()

        client = APIClient()
        client.force_authenticate(user=moderator)

        response = client.post(
            f"/api/v1/moderation/{pending_listing.id}/decision/",
            {
                "decision": "reject",
                "rejection_code": "MOD_101",
                "rejection_note": "reject again",
            },
        )

        assert response.status_code == 400
        assert response.data["error"]["code"] == "MOD_306"

    def test_decision_requires_moderator_role(self, check_holder, pending_listing):
        client = APIClient()
        client.force_authenticate(user=check_holder)

        response = client.post(
            f"/api/v1/moderation/{pending_listing.id}/decision/",
            {"decision": "approve"},
        )

        assert response.status_code == 403

    def test_decision_requires_authentication(self, pending_listing):
        client = APIClient()

        response = client.post(
            f"/api/v1/moderation/{pending_listing.id}/decision/",
            {"decision": "approve"},
        )

        assert response.status_code == 401

    def test_invalid_decision_value_returns_400(self, moderator, pending_listing):
        client = APIClient()
        client.force_authenticate(user=moderator)

        response = client.post(
            f"/api/v1/moderation/{pending_listing.id}/decision/",
            {"decision": "invalid"},
        )

        assert response.status_code == 400

    def test_reject_published_listing_returns_400(self, moderator, published_listing):
        client = APIClient()
        client.force_authenticate(user=moderator)

        response = client.post(
            f"/api/v1/moderation/{published_listing.id}/decision/",
            {
                "decision": "reject",
                "rejection_code": "MOD_101",
                "rejection_note": "should fail",
            },
        )

        assert response.status_code == 400


@pytest.fixture
def rejected_listing(db, check_holder, issuer):
    return ChequeListingFactory.create(
        rejected=True,
        owner=check_holder,
        issuer=issuer,
        bank_name="بانک ملت",
        cheque_serial_number="7777666655554444",
        face_amount=250000000,
        due_date="2026-12-31",
        issuer_type="legal",
        issuer_name="شرکت نمونه",
        issuer_national_id="1234567890",
        resubmit_count=1,
    )


@pytest.mark.django_db
class TestModerationResubmitEndpoint:
    def test_resubmit_rejected_listing_moves_to_pending(self, check_holder, rejected_listing):
        client = APIClient()
        client.force_authenticate(user=check_holder)

        response = client.post(f"/api/v1/moderation/{rejected_listing.id}/resubmit/")

        assert response.status_code == 200
        rejected_listing.refresh_from_db()
        assert rejected_listing.status == ChequeListing.Status.PENDING_MODERATION

    def test_resubmit_non_rejected_listing_returns_400(self, check_holder, pending_listing):
        client = APIClient()
        client.force_authenticate(user=check_holder)

        response = client.post(f"/api/v1/moderation/{pending_listing.id}/resubmit/")

        assert response.status_code == 400
        assert response.data["error"]["code"] == "VALIDATION_ERROR"

    def test_resubmit_at_limit_returns_mod_306(self, check_holder, rejected_listing):
        rejected_listing.resubmit_count = 3
        rejected_listing.save(update_fields=["resubmit_count"])

        client = APIClient()
        client.force_authenticate(user=check_holder)

        response = client.post(f"/api/v1/moderation/{rejected_listing.id}/resubmit/")

        assert response.status_code == 400
        assert response.data["error"]["code"] == "MOD_306"

    def test_resubmit_requires_authentication(self, rejected_listing):
        client = APIClient()

        response = client.post(f"/api/v1/moderation/{rejected_listing.id}/resubmit/")

        assert response.status_code == 401

    def test_resubmit_by_non_owner_returns_403(self, rejected_listing):
        other_user = UserFactory.create()
        client = APIClient()
        client.force_authenticate(user=other_user)

        response = client.post(f"/api/v1/moderation/{rejected_listing.id}/resubmit/")

        assert response.status_code == 403
        assert response.data["error"]["code"] == "PERMISSION_ERROR"
