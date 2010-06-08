from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^mail-a-friend/', include('mailfriend.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'', 'django.views.generic.simple.direct_to_template',
        {'template':'base.html','extra_context':{'superuser':User.objects.all()[0]}}), 
)
