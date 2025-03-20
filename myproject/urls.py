from django.urls import path
from myapp import views

urlpatterns = [
    # ...existing urls...
    path('get_statistics/', views.get_statistics, name='get_statistics'),
    # ...existing urls...
]
