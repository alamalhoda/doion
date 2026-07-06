from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationPreference",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("in_app_enabled", models.BooleanField(default=True)),
                ("sms_enabled", models.BooleanField(default=False)),
                ("email_enabled", models.BooleanField(default=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="notification_preferences", to="users.User")),
            ],
            options={
                "verbose_name": "Notification Preference",
                "verbose_name_plural": "Notification Preferences",
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("type", models.CharField(max_length=30, choices=[("match_created", "Match Created"), ("match_accepted", "Match Accepted"), ("match_declined", "Match Declined"), ("match_cancelled", "Match Cancelled"), ("settlement_confirmed", "Settlement Confirmed"), ("listing_published", "Listing Published"), ("listing_rejected", "Listing Rejected"), ("listing_expired", "Listing Expired"), ("kyc_approved", "KYC Approved"), ("kyc_rejected", "KYC Rejected"), ("new_moderation_item", "New Moderation Item")])),
                ("channel", models.CharField(max_length=20, choices=[("in_app", "In App"), ("sms", "SMS"), ("email", "Email")])),
                ("status", models.CharField(max_length=20, choices=[("pending", "Pending"), ("sent", "Sent"), ("read", "Read"), ("failed", "Failed")], default="pending")),
                ("title", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("related_object_type", models.CharField(max_length=50, null=True, blank=True)),
                ("related_object_id", models.CharField(max_length=255, null=True, blank=True)),
                ("read_at", models.DateTimeField(null=True, blank=True)),
                ("sent_at", models.DateTimeField(null=True, blank=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="users.User")),
            ],
            options={
                "verbose_name": "Notification",
                "verbose_name_plural": "Notifications",
            },
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(fields=["user", "-created_at"], name="notification_user_created_idx"),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(fields=["user", "status", "-created_at"], name="notification_user_status_idx"),
        ),
    ]