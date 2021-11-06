from django.urls import path
from front_end import views

urlpatterns = [
    path('about/', views.about),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.logout),
    path('nexuselectric/', views.NexusElectricView.as_view())
]