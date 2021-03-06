# Generated by Django 2.1 on 2018-08-21 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20180821_0843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stem', models.TextField(unique=True)),
                ('_originals', models.TextField(default='{}')),
                ('tweets', models.ManyToManyField(blank=True, related_name='tokens', to='core.Tweet')),
            ],
        ),
    ]
