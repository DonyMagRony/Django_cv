import platform
import pdfkit
import io

from django.shortcuts import render
from .models import Profile
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404



def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")
        employed = request.POST.get("employed", "")
        if employed == 'on':
            employed = True
        else:
            employed = False
        profile = Profile(name=name, phone=phone, email=email, summary=summary, degree=degree, school=school, university=university, previous_work=previous_work, skills=skills, employed=employed)
        profile.save()
    return render(request, 'pdf/accept.html')


def get_wkhtmltopdf_path():
    os_platform = platform.system()
    if os_platform == "Windows":
        return r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    elif os_platform == "Linux":
        return "/usr/bin/wkhtmltopdf"
    elif os_platform == "Darwin":
        return "/usr/local/bin/wkhtmltopdf"
    return None  

def resume(request, id):
    user_profile = get_object_or_404(Profile, pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile})

    options = {'page-size': 'Letter', 'encoding': 'UTF-8'}
    wkhtmltopdf_path = get_wkhtmltopdf_path()

    if not wkhtmltopdf_path:
        return HttpResponse("wkhtmltopdf not found", status=500)

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    try:
        pdf = pdfkit.from_string(html, False, options=options, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
        return response
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {e}", status=500)

def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles':profiles})

