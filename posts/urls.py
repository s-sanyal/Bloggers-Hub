from django.conf.urls import url
from . import views
app_name='posts'
urlpatterns = [
    # /posts/
    url(r'^$', views.index, name='index'),
    # /posts/<topic_id>
    #url(r'^(?P<topic_id>[0-9]+)/$',views.detail, name='detail'),
    # /posts/<topic_id>/<blog_id>/
    url(r'^(?P<topic_id>[0-9]+)/(?P<blog_id>[0-9]+)/$', views.descriptions, name='descriptions'),
    # /posts/register/
    url(r'^register/$',views.UserFormView.as_view(),name='registration'),
    # /posts/login/
    url(r'^login/$',views.LoginFormView.as_view(),name='login'),
    # /posts/users/<user_id>/
    url(r'^login/users/(?P<user_id>[0-9]+)/$',views.loginmode, name='loginmode'),
    #/posts/add/
     url(r'^add/$',views.AddFormView.as_view(),name='Add'),
    #/posts/<topic_id>/page=<page>
    url(r'^(?P<topic_id>[0-9]+)/page=(?P<page>[0-9]+)/$',views.detail, name='detail'),
     # /posts/logout/
     url(r'^logout/$',views.logout_view,name='logout_view'),
     #/posts/user=<user_id>
     url(r'^users=(?P<user_id>[0-9]+)/$',views.profile_view, name='profile'),
     #/posts/user_check/
     url(r'^user_check/$',views.check, name='check'),
     #/posts/email_check/
     url(r'^email_check/$',views.e_check, name='echeck'),
     #/posts/pp_upload/<user_id>/
    url(r'^pp_upload/(?P<user_id>[0-9]+)/$',views.pp_uploads, name='uploadpp'),
    #/posts/bio_save/<user_id>/
    url(r'^bio_save/(?P<user_id>[0-9]+)/$',views.bio_saves,name='edit_bio'),
    #/posts/cp_upload/<user_id>/
    url(r'^cp_upload/(?P<user_id>[0-9]+)/$',views.cp_uploads, name='uploadcp'),
    #/posts/delete/<blog_id>/
    url(r'^delete/(?P<pk>[0-9]+)/$',views.DeletePosts.as_view(),name='delete'),
    #/posts/update_posts/<blog_id>/
    url(r'^update_posts/(?P<pk>[0-9]+)/$',views.UpdatePost.as_view(),name='update'),
]