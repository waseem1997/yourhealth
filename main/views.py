from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm  # my custome form

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from .decorators import only_doctor, only_patient, both_allowed

from .models import Clinic, Appointment, Category, Article, Category, News

from django.contrib.auth.models import User

# Create your views here.


def home_view(request, cat_id=-1):

    # get all the article:
    context = {}  # main context

    try:
        if cat_id > 0:
            selected_cat = Category.objects.get(id=cat_id)
            list_of_articles = Article.objects.filter(article_category=selected_cat)
        else:
            list_of_articles = Article.objects.all().order_by("-date")

        # also I want to send my Categories:
        list_of_categories = Category.objects.all()
        context["categories"] = list_of_categories
        context["articles"] = list_of_articles

    except:
        context["empty"] = None

    # add the News feed:

    all_news = News.objects.all()

    context["news"] = all_news

    latest_5_doctors = Clinic.objects.all().order_by("-id")[:5]

    context["latest_5"] = latest_5_doctors

    return render(request, "main/pages/home.html", context)


def full_article_view(request, article_id):

    context = {}

    try:
        context["article"] = Article.objects.get(id=article_id)
    except:
        return redirect("/")

    return render(request, "main/pages/full-article.html", context)


# register view:


def register_view(request):

    # registration process

    errors = []
    context = {}
    if request.method == "POST":
        # get form data:
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password1 = make_password(request.POST.get("password"))
        password2 = make_password(request.POST.get("password2"))

        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1,
        )

        if not request.POST.get("password") == request.POST.get("password2"):
            return render(
                request,
                "main/pages/register.html",
                {"errors": "The passwords does not matching"},
            )

        try:
            new_user.save()
        except:
            return render(
                request,
                "main/pages/register.html",
                {"errors": "the username is not valid."},
            )

        is_doctor = request.POST.get("is_doctor")
        is_patient = request.POST.get("is_patient")

        user_group_patient = Group.objects.get(name="patient")
        user_group_doctor = Group.objects.get(name="doctor")

        # check the user group:
        if is_doctor:
            user_group_doctor.user_set.add(new_user)
        else:
            user_group_patient.user_set.add(new_user)

        return redirect("/login/")

    else:
        return render(request, "main/pages/register.html", {})


# login view
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate the use:
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "username OR password is wrong")

    context = {}
    return render(request, "main/pages/login.html", context)


# logout view:


@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect("/")


# doctor dash:
@login_required(login_url="/login")
@only_doctor
def doctor_dash_view(request, state):

    # load all the appointemnts for the doctor:
    # state: 1 --> Requested, 2: Confirmed, 3: Done

    list_of_appointemnts = []

    doctor_id = request.user.id

    if state == 1:  # Requested
        list_of_appointemnts = Appointment.objects.filter(
            clinic__clinic_doctor__id=doctor_id, state="Requested"
        )

    elif state == 2:  # Confirmed
        list_of_appointemnts = Appointment.objects.filter(
            clinic__clinic_doctor__id=doctor_id, state="Confirmed"
        )

    elif state == 3:  # Done
        list_of_appointemnts = Appointment.objects.filter(
            clinic__clinic_doctor__id=doctor_id, state="Canceled"
        )

    else:
        return redirect("/")
    # get clinic state
    clinic_state = False
    try:
        clinic_state = Clinic.objects.get(clinic_doctor__id=doctor_id).activated
    except:
        pass

    context = {"appointments": list_of_appointemnts, "clinic_state": clinic_state}
    return render(request, "main/pages/doctor_dash.html", context)


# patient dash:


@login_required(login_url="/login")
@only_patient
def patient_dash_view(request):

    # load all the patient appointments:
    user_id = request.user.id
    # get he appointments that related to the user
    list_of_appintments = Appointment.objects.filter(patient__id=user_id)

    context = {"appointments": list_of_appintments}
    return render(request, "main/pages/patient_dash.html", context)


@login_required(login_url="/login")
@only_doctor
def confirm_appointment_request_view(request, appointment_id):
    # this view will change the status of the appointment and let the doctor to set the time and the date
    if request.method == "POST":
        # get the data:
        time = request.POST.get("time")
        date = request.POST.get("date")
        description = request.POST.get("description")
        state = "Confirmed"

        # get the appointment:
        selected_appointment = Appointment.objects.get(id=appointment_id)

        selected_appointment.date = date
        selected_appointment.time = time
        selected_appointment.description = description
        selected_appointment.state = state

        print(selected_appointment)
        selected_appointment.save()

        return redirect("/doctor-dash/2/")

    return render(request, "main/pages/confirm_appointment.html", {})


@login_required(login_url="login/")
@only_doctor
def cancel_appointment(request, appointment_id):
    if request.method == "GET":
        if appointment_id > 0:
            selected_appointment = Appointment.objects.get(id=appointment_id)
            selected_appointment.state = "Canceled"
            selected_appointment.save()
            return redirect("/doctor-dash/3")
    return render(request, "main/pages/confirm_appointment.html", {})


# doctor list view: list of all the doctors with a search bar:
# all the users allowd to enter this page (no modification inside it)


def doctors_list_view(request):
    list_of_doctors = []  # list of all the doctors

    if request.method == "POST":
        # get the search word:
        search_word = request.POST.get("search")
        specialization = request.POST.get("specialization")
        province = request.POST.get("province")

        # check_for_search:
        # recieve: name - specialization - province
        # return: list of CLinics
        list_of_doctors = list_of_doctors_search(search_word, specialization, province)

    else:
        list_of_doctors = Clinic.objects.filter(activated=True)  # get all the doctors

    context = {"list_of_doctors": list_of_doctors}
    return render(request, "main/pages/doctors_list.html", context)


# clinic details view
def clinic_details_view(request, clinic_id):
    context = {}
    if clinic_id > 0:
        # here I can get specifci clinci from the database
        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except:
            return HttpResponse("sorry, this request is not exist or incorrect")

        if clinic != None:
            context["clinic"] = clinic
        else:
            return HttpResponse("sorry, this request is not defwe exist or incorrect")
    else:
        return HttpResponse("sorry, this request is not exist or incorrect")

    return render(request, "main/pages/clinic_details.html", context)


# appointment view:


@login_required(login_url="/login")
@both_allowed
def appointment_view(request):

    if request.method == "POST":
        # patient request

        if request.user.groups.all()[0].name == "patient":
            # the user want to request an appointment:
            # I need to create a new appointment object and
            # pass with it the User, Clinic, Status
            patient_id = request.user.id  # get the user ID
            clinic_id = request.POST.get("clinic")
            # get the patient and clinic instances:
            patient = User.objects.filter(id=patient_id)[0]
            clinic = Clinic.objects.filter(id=clinic_id)[0]
            print(clinic, patient)
            # now I can create the new object:
            new_appointemnt_requested = Appointment(
                patient=patient, clinic=clinic, state="Requested"
            )
            new_appointemnt_requested.save()
            return redirect("/patient-dash/")

        # doctor request:
        elif request.user.groups.all()[0].name == "doctor":
            return HttpResponse("this is a doctor request")
        else:
            return redirect("/")

    return HttpResponse("Failed")


# add new clinic view:
@login_required(login_url="/login")
@only_doctor
def new_clinic_view(request):

    if request.method == "POST":
        # get the data:

        speciality = request.POST.get("speciality")
        province = request.POST.get("province")
        location = request.POST.get("location")
        open_time = request.POST.get("open_time")
        close_time = request.POST.get("close_time")
        description = request.POST.get("description")
        phone_number = request.POST.get("phone_number")
        clinic_doctor = request.user

        # create new Clinic object:
        new_clinic = Clinic(
            speciality=speciality,
            phone_number1=phone_number,
            province=province,
            location=location,
            open_time=open_time,
            close_time=close_time,
            description=description,
            clinic_doctor=clinic_doctor,
        )
        new_clinic.save()
        return redirect("/doctors-list/")
    context = {}
    return render(request, "main/pages/create_new_clinic.html", context)


@login_required(login_url="/login")
@only_patient
def appointment_details_view(request, appointment_id):
    context = {}
    # get the appointment details:
    try:
        if isinstance(appointment_id, int):
            selected_appointment = Appointment.objects.get(id=appointment_id)
            context = {"appointment": selected_appointment}
            return render(
                request, "main/pages/appointment_details.html", context=context
            )
        else:
            return HttpResponse("Invalid url")

    except:

        return HttpResponse("Sorry this ID is Wrong.")


@login_required(login_url="login/")
@only_doctor
def new_article_view(request):
    context = {}

    if request.method == "POST":
        # save the article

        article_category_id = request.POST.get("category")
        # get the category object:
        article_category = Category.objects.get(id=article_category_id)
        article_image = request.FILES.get("image")  # get the post image
        article_title = request.POST.get("title")
        article_body = request.POST.get("body")

        new_article = Article(
            article_category=article_category,
            article_author=request.user,
            title=article_title,
            image=article_image,
            body=article_body,
        )

        new_article.save()

        return redirect("/")

    try:
        categories = Category.objects.all()
        context["categories"] = categories
    except:
        return HttpResponse("Error!")

    return render(request, "main/pages/new_article.html", context)


@login_required(login_url="login/")
@only_doctor
def doctor_articles(request):
    context = {}

    if request.method == "POST":
        # delete the article
        selected_article_id = request.POST.get("article")
        print(selected_article_id)
        try:
            article = Article.objects.get(id=selected_article_id)
            article.delete()
            return redirect("/doctor-dash/1/")
        except:
            return HttpResponse("Unexpected Error Occured")

    # here I to send list of all the articles to display then in a  table
    list_of_doctor_articles = []
    try:
        list_of_doctor_articles = Article.objects.filter(article_author=request.user.id)
        context["list_of_articles"] = list_of_doctor_articles
    except:
        context["message"] = "empty"

    return render(request, "main/pages/doctor_articles.html", context)


"""
this function is used to return list of clinic 
based on different seach case of use 
and it's used by the "doctor_list_view"
"""


def list_of_doctors_search(search_word, specialization, province):
    list_of_doctors = []

    if (
        specialization and province == None and search_word == ""
    ):  # search for specialization
        list_of_doctors = Clinic.objects.filter(speciality=specialization)
    elif (
        province and specialization == None and search_word == ""
    ):  # search for provine
        list_of_doctors = Clinic.objects.filter(province=province)
    elif (
        search_word != "" and specialization == None and province == None
    ):  # seach for name:
        list_of_doctors = Clinic.objects.filter(clinic_doctor__first_name=search_word)
    elif (
        province and specialization and search_word == ""
    ):  # search for province and speciality
        list_of_doctors = Clinic.objects.filter(
            province=province, speciality=specialization
        )
    elif (
        province and search_word != "" and specialization == None
    ):  # search for provine and name
        list_of_doctors = Clinic.objects.filter(
            province=province, clinic_doctor__first_name=search_word
        )
    elif (
        specialization and search_word != "" and province == None
    ):  # search for speciality and name
        list_of_doctors = Clinic.objects.filter(
            speciality=specialization, clinic_doctor__first_name=search_word
        )
    elif province and specialization and search_word != "":
        list_of_doctors = Clinic.objects.filter(
            province=province,
            clinic_doctor__first_name=search_word,
            speciality=specialization,
        )
    else:
        list_of_doctors = Clinic.objects.all()

    return list_of_doctors
