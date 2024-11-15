from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # سایر مسیرهای شما
    path('create-order/', views.create_order_with_search, name='create_order'),
    path('search-drug/', views.search_drug, name='search_drug'),
]
