from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    id_str = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True, blank=True)
    screen_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    entities = models.TextField(null=True, blank=True)
    followers_count = models.IntegerField(null=True, blank=True)
    friends_count = models.IntegerField(null=True, blank=True)
    listed_count = models.IntegerField(null=True, blank=True)
    favourites_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    lang = models.CharField(max_length=200, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    background_image_url = models.URLField(null=True, blank=True)
    banner_url = models.URLField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return self.screen_name


class Tweet(models.Model):
    created_at = models.DateTimeField()
    id_str = models.CharField(max_length=200)
    text = models.TextField()
    profile = models.ForeignKey(Profile, related_name='tweets',
                                on_delete=models.CASCADE)
    symbols = models.TextField(null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    geo = models.TextField(null=True, blank=True)
    coordinates = models.TextField(null=True, blank=True)
    place = models.TextField(null=True, blank=True)
    retweet_count = models.IntegerField(null=True, blank=True)
    favorite_count = models.IntegerField(null=True, blank=True)
    lang = models.CharField(max_length=200, null=True, blank=True)
    most_common_word = models.TextField(null=True, blank=True)
    most_common_stem = models.TextField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('tweet')
        verbose_name_plural = _('tweets')

    def __str__(self):
        return self.text


class Mention(models.Model):
    tweets = models.ManyToManyField('core.Tweet', related_name='mentions',
                                    blank=True)

    id_str = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    screen_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("Mention")
        verbose_name_plural = _("Mentions")

    def __str__(self):
        return self.screen_name


class Hashtag(models.Model):
    tweets = models.ManyToManyField('core.Tweet', related_name='hashtags',
                                    blank=True)
    text = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _("Hashtag")
        verbose_name_plural = _("Hashtags")

    def __str__(self):
        return self.text


class Link(models.Model):
    tweets = models.ManyToManyField('core.Tweet', related_name='urls',
                                    blank=True)

    url = models.URLField()
    expanded_url = models.TextField(unique=True)
    display_url = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    collected_metas = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def __str__(self):
        return self.display_url


class Category(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=200)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='children')
    color = ColorField(default='#383838')
    tweets = models.ManyToManyField(Tweet, related_name='categories',
                                    blank=True, null=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Query(models.Model):
    RESULT_TYPE_CHOICES = (
        ('popular', _('Popular')),
        ('recent', _('Recent')),
        ('mixed', _('Mixed'))
    )
    text = models.TextField(verbose_name=_("text"))
    result_type = models.CharField(verbose_name=_("result_type"),
                                   max_length=200, choices=RESULT_TYPE_CHOICES,
                                   default='recent')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='queries')
    lang = models.CharField(max_length=200, null=True, blank=True, default='pt')
    locale = models.CharField(max_length=200, null=True, blank=True)
    until = models.CharField(max_length=200, null=True, blank=True,
                             help_text="YYYY-MM-DD")
    since_id = models.CharField(max_length=200, null=True, blank=True)
    max_id = models.CharField(max_length=200, null=True, blank=True)
    geocode = models.CharField(max_length=200, null=True, blank=True,
                               help_text='latitude longitude radius(mi or km)')

    class Meta:
        verbose_name = _('query')
        verbose_name_plural = _('queries')

    def __str__(self):
        return self.category.name
