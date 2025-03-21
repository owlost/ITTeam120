# Generated by Django 5.1.3 on 2025-03-08 23:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BorrowInfo",
            fields=[
                ("Number", models.AutoField(primary_key=True, serialize=False)),
                (
                    "BorrowTime",
                    models.DateTimeField(auto_now_add=True, verbose_name="借閱時間"),
                ),
                ("ReturnTime", models.DateTimeField(verbose_name="預計歸還時間")),
                (
                    "ActualReturnTime",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="實際歸還時間"
                    ),
                ),
                (
                    "Status",
                    models.CharField(
                        choices=[
                            ("Borrowed", "Borrowed"),
                            ("Returned", "Returned"),
                            ("Overdue", "Overdue"),
                        ],
                        default="Borrowed",
                        max_length=10,
                        verbose_name="狀態",
                    ),
                ),
                (
                    "BookID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="books.book",
                        verbose_name="書籍",
                    ),
                ),
                (
                    "BorrowUserID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="借閱者",
                    ),
                ),
            ],
        ),
    ]
