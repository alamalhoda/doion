from django.db import models, migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SMSLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("phone_number", models.CharField(max_length=20)),
                ("message", models.TextField()),
                ("provider", models.CharField(max_length=20, choices=[("stub", "Stub"), ("kavenegar", "Kavenegar"), ("melipayamak", "Melipayamak")])),
                ("status", models.CharField(max_length=20, choices=[("pending", "Pending"), ("sent", "Sent"), ("failed", "Failed")])),
                ("response", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "SMS Log",
                "verbose_name_plural": "SMS Logs",
            },
        ),
    ]