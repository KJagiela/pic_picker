from django.urls import path

from apps.challenges.views import (
    PicPickerView,
    RegisterVoteView,
)

urlpatterns = [
    path('available_picks/', PicPickerView.as_view()),
    path('vote/', RegisterVoteView.as_view()),
]
