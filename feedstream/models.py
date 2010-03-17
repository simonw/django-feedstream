from django.db import models
from django.utils import simplejson
from django.template import Template, Context
import feedparser, time, datetime

ISO_KEY = '__iso_datetime__'
FORMAT_STRING = '%Y-%m-%dT%H:%M:%S'

class FeedType(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    template = models.TextField()
    default_icon = models.CharField(max_length = 255, blank = True)
    
    def __unicode__(self):
        return self.name
    
class Feed(models.Model):
    type = models.ForeignKey(FeedType)
    name = models.CharField(max_length = 100)
    url = models.CharField(max_length = 255)
    default_icon = models.CharField(max_length = 255, blank = True)
    etag = models.CharField(max_length = 255, blank = True)
    modified = models.CharField(max_length = 255, blank = True)
    last_polled = models.DateTimeField(blank = True, null = True)
    
    def fetch(self):
        kwargs = {}
        if self.etag:
            kwargs['etag'] = self.etag
        if self.modified:
            kwargs['modified'] = time.struct_time(
                map(int, self.modified.split(','))
            )
        
        feed = feedparser.parse(self.url, **kwargs)
        for entry in feed.entries:
            self.add_entry(entry)
        
        self.last_polled = datetime.datetime.now()
        if hasattr(feed, 'etag'):
            self.etag = feed.etag
        if hasattr(feed, 'modified'):
            self.modified = ','.join(map(str, feed.modified))
        self.save()
    
    def add_entry(self, entry):
        guid = entry.guid
        obj, created = self.entries.get_or_create(
            guid = guid,
            defaults = {
                'created': struct_time_to_datetime(entry.updated_parsed),
                'json': simplejson.dumps(
                    entry, indent = 2, default = simplejson_default
                ),
                'title': entry.title,
            }
        )
        return obj
    
    def __unicode__(self):
        return self.url

class Entry(models.Model):
    feed = models.ForeignKey(Feed, related_name = 'entries')
    guid = models.CharField(max_length = 255, unique = True)
    created = models.DateTimeField()
    json = models.TextField()
    title = models.CharField(max_length = 255, blank = True)
    
    @property
    def data(self):
        return simplejson.loads(self.json, object_hook=simplejson_object_hook)
    
    def render(self):
        template = Template(self.feed.type.template)
        return template.render(Context({
            'entry': self.data,
            'feed': self.feed,
        }))
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.guid)

def simplejson_object_hook(dct):
    if ISO_KEY in dct:
        return datetime.datetime.strptime(dct[ISO_KEY], FORMAT_STRING)
    return dct

def simplejson_default(obj):
    if isinstance(obj, time.struct_time):
        return {ISO_KEY: time.strftime(FORMAT_STRING, obj)}
    return obj

def struct_time_to_datetime(st):
    return datetime.datetime.strptime(
        time.strftime(FORMAT_STRING, st), FORMAT_STRING
    )
