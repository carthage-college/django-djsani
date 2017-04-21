from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from djsani.medical_history.waivers import views

urlpatterns = [
    # generic waiver successfull submission redirect
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='medical_history/waivers/success.html'
        ),
        name='waiver_success'
    ),
    # medical history waiver forms
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/(?P<wtype>[a-zA-Z0-9_-]+)/$',
        views.form, name="waiver_form"
    ),
    url(
        r'^$',
        RedirectView.as_view(url=reverse_lazy("home"))
    ),
]
