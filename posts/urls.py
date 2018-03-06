from django.conf.urls import url
from . import views
app_name='posts'
urlpatterns = [
    # /posts/
    url(r'^$', views.index, name='index'),
    # /posts/<topic_id>
    url(r'^(?P<topic_id>[0-9]+)/$',views.detail, name='detail'),
    # /posts/<topic_id>/<blog_id>/
    url(r'^(?P<topic_id>[0-9]+)/(?P<blog_id>[0-9]+)/$', views.descriptions, name='descriptions'),
    # /posts/register/
    url(r'^register/$',views.UserFormView.as_view(),name='registration'),
    # /posts/login/
    url(r'^login/$',views.LoginFormView.as_view(),name='login'),
    # /posts/users/<user_id>/
    url(r'^login/users/(?P<user_id>[0-9]+)/$',views.loginmode, name='loginmode'),
]