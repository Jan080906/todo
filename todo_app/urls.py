from django.urls import URLPattern, path
from . import views

# URLConf
urlpatterns = [
    path('tasks/', views.tasks),
    path('task/<int:id>', views.task)
]