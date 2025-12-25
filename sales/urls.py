from django.urls import path
from .views import home, login_view, logout_view, records, register_view

app_name = 'sales'

urlpatterns = [
   path('', home, name='home'),  
   path('records/', records, name='records'),
   path('login/', login_view, name='login'),
   path('logout/', logout_view, name='logout'),
   path('register/', register_view, name='register'),
]
