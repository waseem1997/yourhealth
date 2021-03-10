from django.http import HttpResponse
from django.shortcuts import redirect

# I want to define the user that logged in to the app (patient, doctor)


def only_doctor(view_func):
    def wrapper_fun(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            print(group)
        if group == "doctor":
            return view_func(request, *args, **kwargs)

        else:
            return redirect("/")

    return wrapper_fun


def only_patient(view_func):
    def wrapper_fun(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            print(group)
        if group == "patient":
            return view_func(request, *args, **kwargs)
        else:
            return redirect("/")

    return wrapper_fun


def both_allowed(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "patient" or "doctor":
            return view_func(request, *args, **kwargs)
        else:
            return redirect("/")

    return wrapper_func