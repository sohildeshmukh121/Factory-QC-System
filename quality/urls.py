
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.create_job, name='create_job'),

    path('inspections/', views.inspection_list, name='inspection_list'),
    path(
        'inspections/create/',
        views.create_inspection,
        name='create_inspection'
    ),
    path(
        'inspections/<int:inspection_id>/<str:decision>/',
        views.review_inspection,
        name='review_inspection'
    ),

    path('dispatch/', views.dispatch_clearance, name='dispatch_clearance'),
]
