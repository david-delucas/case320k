from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import BusinessCase, BusinessCaseCategory, BusinessCaseSeries
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.conf import settings
from django.views.generic.base import TemplateView
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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

    _redirect_name = "main:"+single_slug
    return redirect(_redirect_name)


def homepage(request):
    return render(request=request,
                  template_name='main/categories.html',
                  context={"categories": BusinessCaseCategory.objects.all
                  })



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

def charge(request): # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'main/charge.html')                    

    form = NewUserForm
    return render(request = request,
                    template_name = "main/charge.html",
                    context={"form":form,
                             "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
                    })



def workflow(request):
    return render(request, 'main/workflow.html')


def graph(request):
    return render(request, 'main/graph.html')

from rest_pandas import PandasView
from .models import TimeSeries
from .serializers import TimeSeriesSerializer, MyCustomPandasSerializer
from rest_pandas.renderers import PandasCSVRenderer, PandasExcelRenderer
from django.http import JsonResponse
# Short version (leverages default DRP settings):
class TimeSeriesView(PandasView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer
    # That's it!  The view will be able to export the model dataset to any of
    # the included formats listed above.  No further customization is needed to
    # leverage the defaults.
    

class Dummy:
    def get(self, request, *args, **kwargs):
        df = self.queryset.to_dataframe()
        serializer_data = self.serializer_class.data
        #return df.to_json()
        #return JsonResponse(list(self.get_queryset()), safe=False)
        return JsonResponse(serializer_data, safe=False)

# Long Version and step-by-step explanation
class TimeSeriesViewLong(PandasView):
    # Assign a default model queryset to the view
    queryset = TimeSeries.objects.all()

    # Step 1. In response to get(), the underlying Django REST Framework view
    # will load the queryset and then pass it to the following function.
    def filter_queryset(self, qs): 
        # At this point, you can filter queryset based on self.request or other
        # settings (useful for limiting memory usage).  This function can be
        # omitted if you are using a filter backend or do not need filtering.
        return qs
        
    # Step 2. A Django REST Framework serializer class should serialize each
    # row in the queryset into a simple dict format.  A simple ModelSerializer
    # should be sufficient for most cases.
    serializer_class = TimeSeriesSerializer  # extends ModelSerializer

    # Step 3.  The included PandasSerializer will load all of the row dicts
    # into array and convert the array into a pandas DataFrame.  The DataFrame
    # is essentially an intermediate format between Step 2 (dict) and Step 4
    # (output format).  The default DataFrame simply maps each model field to a
    # column heading, and will be sufficient in many cases.  If you do not need
    # to transform the dataframe, you can skip to step 4.
    
    # If you would like to transform the dataframe (e.g. to pivot or add
    # columns), you can do so in one of two ways:

    # A. Create a subclass of PandasSerializer, define a function called
    # transform_dataframe(self, dataframe) on the subclass, and assign it to
    # pandas_serializer_class on the view.  You can also use one of the three
    # provided pivoting serializers (see Advanced Usage below).
    #
    # class MyCustomPandasSerializer(PandasSerializer):
    #     def transform_dataframe(self, dataframe):
    #         dataframe.some_pivot_function(in_place=True)
    #         return dataframe
    #
    pandas_serializer_class = MyCustomPandasSerializer

    # B. Alternatively, you can create a custom transform_dataframe function
    # directly on the view.  Again, if no custom transformations are needed,
    # this function does not need to be defined.
    def transform_dataframe(self, dataframe):
        dataframe.some_pivot_function(in_place=True)
        return dataframe
    
    # NOTE: As the name implies, the primary purpose of transform_dataframe()
    # is to apply a transformation to an existing dataframe.  In PandasView,
    # this dataframe is created by serializing data queried from a Django
    # model.  If you would like to supply your own custom DataFrame from the
    # start (without using a Django model), you can do so with PandasSimpleView
    # as shown in the first example.

    # Step 4. Finally, the provided renderer classes will convert the DataFrame
    # to any of the supported output formats (see above).  By default, all of
    # the formats above are enabled.  To restrict output to only the formats
    # you are interested in, you can define renderer_classes on the view:
    renderer_classes = [PandasCSVRenderer, PandasExcelRenderer]
    # You can also set the default renderers for all of your pandas views by
    # defining the PANDAS_RENDERERS in your settings.py.

    # Step 5 (Optional).  The default filename may not be particularly useful
    # for your users.  To override, define get_pandas_filename() on your view.
    # If a filename is returned, rest_pandas will include the following header:
    # 'Content-Disposition: attachment; filename="Data Export.xlsx"'
    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            # Use custom filename and Content-Disposition header
            return "Data Export"  # Extension will be appended automatically
        else:
            # Default filename from URL (no Content-Disposition header)
            return None