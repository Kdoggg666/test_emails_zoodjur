from django.urls import path
from . import views


urlpatterns = [
     path('', views.all_animals, name='animals'),
     path('<int:animal_id>/', views.animal_details, name='animal_details'),
     path('add/', views.add_animal, name='add_animal'),
     path('edit/<int:animal_id>/', views.edit_animal, name='edit_animal'),
     path('delete/<int:animal_id>/', views.delete_animal,
          name='delete_animal'),
     path('add_review/<int:animal_id>/', views.add_review, name='add_review'),
     path('edit_review/<int:animal_id>/<int:review_id>/', views.edit_review,
          name='edit_review'),
     path('delete_review/<int:animal_id>/<int:review_id>/',
          views.delete_review, name='delete_review'),
]
