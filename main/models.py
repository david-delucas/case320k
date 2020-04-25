from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Customer(models.Model):
    customer = models.IntegerField("Customer ID",default=0)
    class Meta:
        verbose_name_plural = "Customers"

    def __str__(self):
        return str(self.customer)


class BusinessCaseCategory(models.Model):
    customer = models.ForeignKey(Customer, default=1, verbose_name="Customer ID", on_delete=models.SET_DEFAULT)
    bc_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200, default="cat1")

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.bc_category


class BusinessCaseSeries(models.Model):
    customer = models.ForeignKey(Customer, default=1, verbose_name="Customer ID", on_delete=models.SET_DEFAULT)    
    bc_series = models.CharField(max_length=200)

    bc_category = models.ForeignKey(BusinessCaseCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "Seriess in admin"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.bc_series

class BusinessCase(models.Model):
    customer = models.ForeignKey(Customer, default=1, verbose_name="Customer ID", on_delete=models.SET_DEFAULT)    
    bc_name = models.CharField(max_length=200)
    bc_description = models.TextField()
    bc_creation_datetime = models.DateTimeField("Creation date", default=timezone.now())
    #https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    bc_series = models.ForeignKey(BusinessCaseSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
    bc_slug = models.CharField(max_length=200, default="bc1")

    def __str__(self):
        return self.bc_name



class ProcessFlowDef(models.Model):
    customer = models.ForeignKey(Customer, default=1, verbose_name="Customer ID", on_delete=models.SET_DEFAULT)    
    proc_def_name = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "Seriess in admin"
        verbose_name_plural = "ProcessFlowDefs"



from django_pandas.managers import DataFrameManager
class TimeSeries(models.Model):
    customer = models.ForeignKey(Customer, default=1, verbose_name="Customer ID", on_delete=models.SET_DEFAULT)    
    date = models.DateTimeField("Date", default=timezone.now())
    full_name = models.CharField(max_length=25, default="")
    age = models.IntegerField("Age",default=0)
    department = models.CharField(max_length=30, default="Default Dept1")
    wage = models.FloatField("Wage",default=0.0)

    objects = DataFrameManager()

    class Meta:
        # otherwise we get "Seriess in admin"
        verbose_name_plural = "TimeSeries"




class Question(models.Model):
    customer = models.ForeignKey(Customer, default=1, verbose_name="Customer ID", on_delete=models.SET_DEFAULT)    
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    customer = models.ForeignKey(Customer, default=1, verbose_name="Customer ID", on_delete=models.SET_DEFAULT)    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


"""[summary]

>>> from polls.models import Choice, Question

# Make sure our __str__() addition worked.
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>

# Django provides a rich database lookup API that's entirely driven by
# keyword arguments.
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith='What')
<QuerySet [<Question: What's up?>]>

# Get the question that was published this year.
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>

# Request an ID that doesn't exist, this will raise an exception.
>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

# Lookup by a primary key is the most common case, so Django provides a
# shortcut for primary-key exact lookups.
# The following is identical to Question.objects.get(id=1).
>>> Question.objects.get(pk=1)
<Question: What's up?>

# Make sure our custom method worked.
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set to hold the "other side" of a ForeignKey relation
# (e.g. a question's choice) which can be accessed via the API.
>>> q = Question.objects.get(pk=1)

# Display any choices from the related object set -- none so far.
>>> q.choice_set.all()
<QuerySet []>

# Create three choices.
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

# Choice objects have API access to their related Question objects.
>>> c.question
<Question: What's up?>

# And vice versa: Question objects get access to Choice objects.
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

# Let's delete one of the choices. Use delete() for that.
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()

"""