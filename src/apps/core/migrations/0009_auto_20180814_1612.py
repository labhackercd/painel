# Generated by Django 2.1 on 2018-08-14 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_tweet_is_processed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Hashtag',
                'verbose_name_plural': 'Hashtags',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('expanded_url', models.URLField(unique=True)),
                ('display_url', models.URLField()),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_str', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('screen_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Mention',
                'verbose_name_plural': 'Mentions',
            },
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='hashtags',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='urls',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='user_mentions',
        ),
        migrations.AddField(
            model_name='mention',
            name='tweets',
            field=models.ManyToManyField(blank=True, related_name='mentions', to='core.Tweet'),
        ),
        migrations.AddField(
            model_name='link',
            name='tweets',
            field=models.ManyToManyField(blank=True, related_name='urls', to='core.Tweet'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tweets',
            field=models.ManyToManyField(blank=True, related_name='hashtags', to='core.Tweet'),
        ),
    ]
