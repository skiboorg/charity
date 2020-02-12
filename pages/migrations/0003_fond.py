# Generated by Django 3.0.2 on 2020-02-12 15:00

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_banner_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название фонда')),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, upload_to='fond/', verbose_name='Лого фонда')),
                ('description_short', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Описание для окна покупки')),
                ('description_full', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Полное описание')),
                ('description_contact', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Контакты')),
            ],
            options={
                'verbose_name': 'Фонд',
                'verbose_name_plural': 'Фонды',
            },
        ),
    ]
