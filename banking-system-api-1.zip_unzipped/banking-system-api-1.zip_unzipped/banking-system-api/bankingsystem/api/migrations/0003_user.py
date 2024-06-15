# Generated by Django 5.0.6 on 2024-05-27 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_transaction_pending'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
    ]