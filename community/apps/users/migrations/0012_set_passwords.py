# Django
from django.contrib.auth.hashers import make_password
from django.db import migrations


# Main Section
def forwards_set_passwords(apps, schema_editor):
    User = apps.get_model("users", "User")

    # Main Migration
    admin_user_info_list = [
        {
            "email": "admin@runners.im",
            "password": "run1234!",
        },
        {
            "email": "sun@runners.im",
            "password": "run1234!",
        },
        {
            "email": "jerry@runners.im",
            "password": "run1234!",
        },
        {
            "email": "andy@runners.im",
            "password": "run1234!",
        },
        {
            "email": "rosie@runners.im",
            "password": "run1234!",
        },
        {
            "email": "liam@runners.im",
            "password": "run1234!",
        },
        {
            "email": "oliver@runners.im",
            "password": "run1234!",
        },
        {
            "email": "bang@runners.im",
            "password": "run1234!",
        },
        {
            "email": "jayden@runners.im",
            "password": "run1234!",
        }
    ]

    # Admin user password update
    for admin_info in admin_user_info_list:
        try:
            user = User.objects.get(email=admin_info["email"])
            user.password = make_password(admin_info["password"])
            user.is_staff = True
            user.is_superuser = True
            user.save()
        except:
            pass


def reverse_set_passwords(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_auto_20240724_0254"),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_set_passwords,
            reverse_code=reverse_set_passwords,
        ),
    ]
