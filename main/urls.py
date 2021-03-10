from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from django.conf import settings

from .views import (
    home_view,
    login_view,
    register_view,
    logout_view,
    doctor_dash_view,
    patient_dash_view,
    doctors_list_view,
    clinic_details_view,
    appointment_view,
    confirm_appointment_request_view,
    cancel_appointment,
    new_clinic_view,
    appointment_details_view,
    new_article_view,
    full_article_view,
    doctor_articles,
)

urlpatterns = [
    path("", home_view),
    path("<int:cat_id>/", home_view, name="home"),  # add the home page
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view),
    path("doctor-dash/<int:state>/", doctor_dash_view),
    path("patient-dash/", patient_dash_view),
    path("doctors-list/", doctors_list_view),
    path("clinic-details/<int:clinic_id>/", clinic_details_view),
    path("appointment/", appointment_view),
    path("confirm-appointment/<int:appointment_id>/", confirm_appointment_request_view),
    path("cancel-appointment/<int:appointment_id>", cancel_appointment),
    path("create-new-clinic/", new_clinic_view),
    path("appointment-details/<int:appointment_id>", appointment_details_view),
    path("create-new-article/", new_article_view),
    path("full-article/<int:article_id>/", full_article_view),
    path("doctor-articles/", doctor_articles),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
