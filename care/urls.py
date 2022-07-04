from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_animals_care, name='all_animals_care'),
    path('<int:animal_id>/', views.animal_care, name='animal_care'),
    path('add_care/<int:animal_id>/', views.add_care, name='add_care'),
    path('edit_care/<int:animal_id>/', views.edit_care, name='edit_care'),
    path('delete_care/<int:animal_id>/',
         views.delete_care, name='delete_care'),
]
