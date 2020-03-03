# Generated by Django 3.0.2 on 2020-03-01 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0011_auto_20200301_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_by', models.CharField(blank=True, max_length=100, null=True, verbose_name='Оплата через')),
                ('isPayed', models.BooleanField(default=False, verbose_name='Оплачен?')),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='item.Item')),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]