from django.urls import path

from .views import TestView
from .views import CollectionDetailView
from .views import CollectionDetailView, CollectionListView


app_name = 'api'
urlpatterns = [
    path('test', TestView.as_view(), name='test')
        path('collections/<int:pk>/',
        CollectionDetailView.as_view(),
        name='collection-detail'),
    path('collections/',
         CollectionListView.as_view(),
         name='collection-list'),
    path('collections/<int:pk>/',
         CollectionDetailView.as_view(),
         name='collection-detail'),
]
