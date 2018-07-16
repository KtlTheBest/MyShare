from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    # /music/
    url(r'^$', views.IndexPage.as_view(), name='index'),

    # /music/add
    url(r'^add/$', views.AddSong.as_view(), name='add_song'),

    # /music/<pk>
    url(r'^(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='details'),

    # /music/<pk>/delete
    url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteSong.as_view(), name='delete'),

    # /music/signup
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),

    # /music/login
    url(r'^login/$', views.LoginView.as_view(), name='login'),

    # /music/logout
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    # /music/profile
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
]
