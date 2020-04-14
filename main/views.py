from django.shortcuts import render
from django.http import HttpResponse
from .models import BusinessCase
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='main/home.html',
                  context = {"business_cases":BusinessCase.objects.all})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})