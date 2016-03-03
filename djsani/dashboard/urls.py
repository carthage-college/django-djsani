from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djsani.dashboard.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='dashboard/success.html'
        ),
        name='admin_success'
    ),
    # ajax communication to paint the panels
    url(
        r'^panels/$',
        'panels', name="dashboard_panels"
    ),
    # ajax returns students because using home view is a
    # pain in the ass with security involved & spinner
    url(
        r'^get-students/$',
        'get_students', name="get_students"
    ),
    # simple ID search
    url(
        r'^student/$',
        'student_detail', name="student_search"
    ),
    # name search
    url(
        r'^student/search/$',
        'advanced_search', name="advanced_search"
    ),
    # student detail
    url(
        r'^student/(?P<cid>\d+)/$',
        'student_detail', name="student_detail"
    ),
    # student detail print
    url(
        r'^student/(?P<cid>\d+)/print/(?P<content>[-\w]+)/$',
        'student_detail',
        name="student_detail_print"
    ),
    # home
    url(
        r'^$', 'home', name="dashboard_home"
    ),
)
