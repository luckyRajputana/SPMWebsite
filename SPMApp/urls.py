from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.MainPage, name='MainPage'),
    path('getmodeldetails/', views.FetchModelDetails, name='FetchModelDetails'),
    path('getmodeldetails/<int:pk>/delete/', views.RowDeleteView, name='Row_delete'),
    path('get_column_data/', views.GetColumnDataView, name='get_column_data'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)