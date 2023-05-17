from django.urls import path

from apps.users.views import (
    RegisterVoterView,
)

urlpatterns = [
    path('users/', RegisterVoterView.as_view()),
]
