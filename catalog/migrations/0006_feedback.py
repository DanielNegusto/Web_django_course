# Generated by Django 5.1.2 on 2024-10-29 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_rename_name_contact_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
            },
        ),
    ]