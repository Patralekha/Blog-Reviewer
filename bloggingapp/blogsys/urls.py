from django.conf.urls import url,include
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
  path('',views.index,name="index"),
  path('newblog',views.newblog,name="newblog"),
  path('createblog',views.create_blog,name="create_blog"),
  path('<int:blogid>',views.blog,name="blogd"),
  path('comment/<int:blogid>',views.submit_comment,name="comment"),
  path('like/<int:blogid>/<int:userpreference>',views.submit_like,name="like"),
  path("login", views.login_request, name="login"),
  path("logout", views.logout_request, name="logout"),
  path("registration", views.registration, name="registration"),
  path("register", views.register, name="register")

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

#if settings.DEBUG: # new
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
