# Generated by Django 2.1 on 2018-08-16 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180814_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='collected_metas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='link',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='site_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
