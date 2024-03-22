# Generated by Django 5.0.3 on 2024-03-21 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="friendrequest",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterField(
            model_name="friendrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("REQUESTED", "Requested"),
                    ("ACCEPTED", "Accepted"),
                    ("REJECTED", "Rejected"),
                ],
                default="REQUESTED",
                max_length=20,
            ),
        ),
    ]
