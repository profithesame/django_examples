"""
URL configuration for profithesame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.utils.translation import gettext_lazy as _
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from blog.sitemaps import PostSitemap
from payment import webhooks

sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    re_path(r'^blog/', include('blog.urls')),
    re_path(
        r'^sitemap\.xml$',
        sitemap,
        {'sitemaps':sitemaps},
        name='django.contrib.sitemaps.views.sitemaps'),
    path(_('account/'), include('account.urls')),
    path('social-auth/',
        include('social_django.urls', namespace='social')),
    path(_('images/'), include('images.urls', namespace='images')),
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path(_('payment/'), include('payment.urls', namespace='payment')),
    path(_('coupons/'), include('coupons.urls', namespace='coupons')),
    path('rosetta', include('rosetta.urls')),
    path('course/', include('courses.urls')),
    path('students/', include('students.urls')),
    path('api/', include('courses.api.urls', namespace='api')),
    path('', include('shop.urls', namespace='shop')),
)

urlpatterns += [path('payment/webhook/', webhooks.stripe_webhook,
    name='stripe-webhook')]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
