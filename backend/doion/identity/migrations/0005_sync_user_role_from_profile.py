from django.db import migrations


def copy_profile_role_to_user(apps, schema_editor):
    Profile = apps.get_model("identity", "Profile")
    User = apps.get_model("users", "User")
    for profile in Profile.objects.iterator():
        User.objects.filter(pk=profile.user_id).exclude(role=profile.role).update(role=profile.role)


def noop_reverse(apps, schema_editor):
    return None


class Migration(migrations.Migration):
    dependencies = [
        ("identity", "0004_profile_user_type_and_national_id_length"),
        ("users", "0003_user_role"),
    ]

    operations = [
        migrations.RunPython(copy_profile_role_to_user, noop_reverse),
    ]
