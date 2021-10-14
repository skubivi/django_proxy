from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^server', ChangeServer.as_view()),
    url(r'^', Request.as_view())

]