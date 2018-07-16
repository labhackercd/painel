from django.urls import path
from apps.core import views


urlpatterns = [
    path('wordcloud/', views.wordcloud),
]
