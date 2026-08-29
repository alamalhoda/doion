from django.db import migrations

from doion.banks.services import backfill_listing_banks


def forwards(apps, schema_editor):
    backfill_listing_banks()


def backwards(apps, schema_editor):
    ChequeListing = apps.get_model("checks", "ChequeListing")
    ChequeListing.objects.update(bank=None)


class Migration(migrations.Migration):

    dependencies = [
        ("checks", "0004_chequelisting_bank"),
        ("banks", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
