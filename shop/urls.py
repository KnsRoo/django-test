from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'shop'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('cats', views.cats, name='cats'),
    url('goods', views.goods, name='goods'),
    url('savecat', views.savecat, name='savecat'),
    url('newedit', views.newedit, name='newedit'),
    url('log_out', views.log_out, name='log_out'),
    url('log_in', views.log_in, name='log_in'),
    url('addGood', views.addGood, name='addGood'),
    url('editGood', views.editGood, name='editGood')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)