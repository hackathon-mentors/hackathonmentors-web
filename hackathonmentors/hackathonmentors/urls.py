from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.views import generic

from hackathonmentors import views

urlpatterns = [
    path('', views.BaseView.as_view(template_name="index.html"), name="index"),
    path('code-of-conduct', views.BaseView.as_view(template_name="coc.html"), name="coc"),
    path('user/', include('user.urls')),
    path('hackathons/', include('hackathon.urls')),
    path('mentors/', include('mentor.urls')),
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('img/favicon.ico'))),
    path(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=TModel,
            create_field='name',
        ),
        name='select2_one_to_one_autocomplete',
    ),
    path(
        'test/(?P<pk>\d+)/$',
        generic.UpdateView.as_view(
            model=TModel,
            form_class=TForm,
        )
    ),
]
