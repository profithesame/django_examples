from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post


class LatestPostsFeed(Feed):
    title = 'Blog about energy gel from Moldova'
    link = '/blog/'
    description = 'New posts of energy moldavian blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item) -> str:
        return item.title
    
    def item_description(self, item) -> str:
        return truncatewords(item.body, 30)
