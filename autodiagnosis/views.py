from django.shortcuts import render, HttpResponse
from .models import Gender, Origin, Symptom, Report, Correlated_Report


def auto_diagnosis_system_view(request):
    context = {}

    selected_gender_id = request.POST.get("gender")
    selected_origin_id = request.POST.get("origin")
    selected_questions_ids = request.POST.getlist("question")  # all the answers

    if request.method == "POST":
        if selected_gender_id:
            selected_gender = Gender.objects.get(id=selected_gender_id)
            all_type_gender = Gender.objects.get(gender="all")
            context["origins"] = Origin.objects.filter(
                gender__in=[selected_gender, all_type_gender]
            )

        if selected_origin_id:
            selected_origin_id = request.POST.get("origin")
            selected_origin = Origin.objects.get(id=selected_origin_id)
            # get the questions:
            questions = Symptom.objects.filter(origin=selected_origin)
            context["questions"] = questions

        if selected_questions_ids:

            # get the reports and the possible diseases
            possible_reports = Correlated_Report.objects.filter(
                symptom__id__in=list(map(int, selected_questions_ids))
            )
            context["reports"] = remove_duplicated(possible_reports)
    else:
        # stage 1: ask for gender
        genders = Gender.objects.all()
        context["gender"] = genders

        print(context["gender"])

    return render(request, "auto_diagnosis/diagnosis.html", context)


def report_view(request, id):
    # get the report from the database:

    report = Correlated_Report.objects.get(id=id)
    context = {}

    if report:
        context["report"] = report
    else:
        return HttpResponse("Error 404!!, please go back to home page.")
    return render(request, "auto_diagnosis/report.html", context=context)


"""
the idea of the auto diagnosis system: 

the user will select the gender 

then the oragin 

then the sympotomth 

now, based on the selections of the user symptomths the system will print out the corrlated reposrt that linked with this 
symptomths: 



"""


# to remove the duplicated disease from the list of possible diseases
# it will return new list without duplicated objects
def remove_duplicated(myList):
    seen_titles = set()
    new_list = []
    for obj in myList:
        if obj.report.report_title not in seen_titles:
            new_list.append(obj)
            seen_titles.add(obj.report.report_title)
    return new_list
