from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Clinic(models.Model):
    # my fields:
    creation_date = models.DateField(auto_now=True, null=True)
    speciality = models.CharField(max_length=255, null=False)
    location = models.CharField(max_length=255, null=False)
    open_time = models.CharField(max_length=255, null=True)
    close_time = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    phone_number1 = models.CharField(max_length=255, null=True, blank=True)
    phone_number2 = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255)
    # foriegn key to the doctor and just for the doctors
    activated = models.BooleanField(default=False)
    clinic_doctor = models.ForeignKey(
        User,  limit_choices_to={'groups__name': "doctor"}, on_delete=models.CASCADE)

    def __str__(self):
        return "clinic of " + self.clinic_doctor.username + ' (' + str(self.creation_date) + ')'


class Appointment(models.Model):
    patient = models.ForeignKey(User, limit_choices_to={
                                'groups__name': "patient"}, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, null=False)
    date = models.CharField(max_length=255, null=False)
    time = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Category(models.Model):
    category = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.category


class Article(models.Model):
    title = models.CharField(max_length=250, null=False)
    body = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now=True)
    article_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    article_author = models.ForeignKey(to=User, limit_choices_to={
                                       'groups__name': 'doctor'}, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class News(models.Model):

    date = models.TimeField(auto_now=True)
    item = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.item
