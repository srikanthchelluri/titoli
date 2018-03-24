from django.urls import path
from . import views

urlpatterns = [
	path('subs/', views.subs, name='subs'),
	path('files/', views.files, name='files')
]
