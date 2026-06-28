from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from doion.core.models import TimeStampedModel


class Document(TimeStampedModel):
    class DocumentType(models.TextChoices):
        NATIONAL_ID_FRONT = "national_id_front", _("National ID Front")
        NATIONAL_ID_BACK = "national_id_back", _("National ID Back")
        SELFIE = "selfie", _("Selfie")
        CHEQUE_IMAGE = "cheque_image", _("Cheque Image")
        ID_DOCUMENT = "id_document", _("ID Document")
        SUPPLEMENTARY = "supplementary", _("Supplementary")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    related_object_type = models.CharField(max_length=50)
    related_object_id = models.CharField(max_length=255)
    document_type = models.CharField(max_length=30, choices=DocumentType.choices)
    file = models.FileField(upload_to="documents/%Y/%m/%d/")
    file_size = models.PositiveIntegerField(help_text=_("File size in bytes"))

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        indexes = [
            models.Index(fields=["related_object_type", "related_object_id"]),
            models.Index(fields=["document_type"]),
        ]

    def __str__(self):
        return f"{self.owner.username} - {self.document_type}"
