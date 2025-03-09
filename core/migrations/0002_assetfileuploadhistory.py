# Generated by Django 5.1.5 on 2025-03-09 15:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetFileUploadHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_file', models.FileField(upload_to='uploaded files')),
                ('validated_file', models.FileField(null=True, upload_to='validated files')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_upload_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
