feedstream
==========

An RSS aggregator / republisher for Django, output easily 
customised using Django's template language.

Depends on feedparser - I suggest a checkout from Subversion, as the 
official release is several years old.

svn checkout http://feedparser.googlecode.com/svn/trunk/ feedparser-read-only

Usage:

Use the admin to add a FeedType with name "Twitter" and template:

    <li class="quote" title="{{ entry.updated_parsed|date:"jS F Y, H:ia" }}">
        <p><a href="{{ entry.url }}" class="meta">{{ feed.name }} said</a>
        {{ entry.title }}
        <span class="meta">{{ entry.updated_parsed|timesince }}</span></p>
    </li>

Add a Feed of that type with URL:

http://pipes.yahoo.com/pipes/pipe.run?
  _id=2705f722f5f53c813b90bbbe0fabbcf3&_render=rss&username=simonw

Swap in your own Twitter username - the Yahoo! pipe just cleans up Twitter's
default RSS feed to remove some cruft and filter out @replies etc.

Run ./manage.py feedstream_fetch to fetch the most recent entries.

In a view function, do this:

    from feedstream.models import Entry

    def index(request):
        return render('index.html', {
            'entries': Entry.objects.order_by('-created')[:20],
        })

In a template, do this:

    <ul>
        {% for entry in feed_entries %}
        {{ entry.render|safe }}
        {% endfor %}
    </ul>
