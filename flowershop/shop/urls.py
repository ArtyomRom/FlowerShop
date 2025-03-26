from django.urls import path
from .views import sales_statistics

urlpatterns = [
    path('sales-statistics/', sales_statistics, name='sales_statistics'),
]