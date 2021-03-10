from django.urls import path
from autodiagnosis.views import auto_diagnosis_system_view, report_view

urlpatterns = [
    path("auto-diagnosis-system/", auto_diagnosis_system_view),
    path("report/<int:id>/", report_view),
]
