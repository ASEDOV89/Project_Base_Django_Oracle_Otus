from django.urls import path
from .views import (
    HomeView,
    CommentsView,
    SubmitCommentView,
    GenerateReportView
    # DownloadReportView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('comments/', CommentsView.as_view(), name='comments'),
    path('submit_comment/', SubmitCommentView.as_view(), name='submit_comment'),
    path('generate_report/', GenerateReportView.as_view(), name='generate_report'),
    # path('download_report/', DownloadReportView.as_view(), name='download_report'),
]