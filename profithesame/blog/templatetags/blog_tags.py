from django import template
from django.db.models import Count

from ..models import Post


register = template.Library()


@register.simple_tag
def total_posts() -> int:
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5) -> dict:
    latest_posts = Post.published.order_by('-publish')[:count]
    return {
        'latest_posts': latest_posts
    }

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
            total_posts=Count('comments')
        ).order_by('-comments'
        )[:count]
    
