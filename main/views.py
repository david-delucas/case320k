from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import BusinessCase, BusinessCaseCategory, BusinessCaseSeries
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.
def single_slug(request, single_slug):
    # first check to see if the url is in categories.
    categories = [c.category_slug for c in BusinessCaseCategory.objects.all()]
    if single_slug in categories:
        matching_series = BusinessCaseSeries.objects.filter(bc_category__category_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = BusinessCase.objects.filter(bc_series__bc_series=m.bc_series).earliest("bc_creation_datetime")
            series_urls[m] = part_one.bc_slug

        return render(request=request,
                      template_name='main/category.html',
                      context={"bc_series": matching_series, "part_ones": series_urls})



    business_cases = [t.bc_slug for t in BusinessCase.objects.all()]

    if single_slug in business_cases:
        this_business_case = BusinessCase.objects.get(bc_slug=single_slug)
        bc_from_series = BusinessCase.objects.filter(bc_series__bc_series=this_business_case.bc_series).order_by('bc_creation_datetime')
        this_bc_idx = list(bc_from_series).index(this_business_case)

        return render(request = request,
                      template_name='main/business_case.html',
                      context = {"business_case":this_business_case,
                               "sidebar": bc_from_series,
                               "this_bc_idx": this_bc_idx})


def homepage(request):
    return render(request=request,
                  template_name='main/categories.html',
                  context={"categories": BusinessCaseCategory.objects.all})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account created: {username}")
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.info(request, f"You are now logged in as: {username}")
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out sucessfully")
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})                  