# Generated by Django 1.9 on 2016-02-10 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Thing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("big", models.BooleanField(default=False)),
                ("clever", models.BooleanField(default=False)),
                (
                    "element_type",
                    models.CharField(
                        choices=[
                            (b"e", b"Earth"),
                            (b"w", b"Water"),
                            (b"a", b"Air"),
                            (b"f", b"Fire"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "category",
                    models.IntegerField(
                        choices=[(0, b"Magma"), (1, b"Quasigroup"), (2, b"Monoid")],
                        default=0,
                    ),
                ),
                ("count", models.IntegerField(default=0)),
                ("description", models.TextField(blank=True)),
                (
                    "notes_file",
                    models.FileField(blank=True, upload_to=b"django_functest/tests/uploads"),
                ),
            ],
        ),
    ]
