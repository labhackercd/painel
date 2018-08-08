from django.urls import path
from apps.core import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('wordcloud/', views.wordcloud),
    path('areachart/', views.areachart),
    path('top-profiles/', views.top_profiles),
]
