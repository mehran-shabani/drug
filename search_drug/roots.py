# search_drug/roots.py
from django.urls import path
from .views import DrugSearchView, DrugDetailView

urlpatterns = [
    path('search/', DrugSearchView.as_view(), name='drug-search'),
    path('<int:id>/', DrugDetailView.as_view(), name='drug-detail'),
]