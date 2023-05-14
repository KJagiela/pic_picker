from django.urls import path

from apps.challenges.views import PicPickerView

urlpatterns = [path('available_picks/', PicPickerView.as_view())]
