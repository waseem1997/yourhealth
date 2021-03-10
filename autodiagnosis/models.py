from django.db import models


class Gender(models.Model):
    gender = models.CharField(max_length=250, null=False, unique=True)

    def getGender(self):
        if self.gender != "all":
            return self.gender
        else:
            return None

    def __str__(self):
        return self.gender


class Origin(models.Model):
    origin = models.CharField(max_length=250, null=False, unique=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    def __str__(self):
        return self.origin


class Symptom(models.Model):
    question = models.CharField(max_length=500, null=True)
    origin = models.ForeignKey(Origin, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Report(models.Model):

    report_title = models.CharField(max_length=500, null=False)
    report_body = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.report_title


class Correlated_Report(models.Model):

    symptom = models.ForeignKey(to=Symptom, on_delete=models.CASCADE)
    report = models.ForeignKey(to=Report, on_delete=models.CASCADE)

    def __str__(self):
        return self.report.report_title
