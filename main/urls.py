"""case320k URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("charge/", views.charge, name="charge"),
    path("slug/<single_slug>", views.single_slug, name="single_slug"),
    path('data/', views.TimeSeriesView.as_view(),name="data"),
    path('graph/', views.graph, name="graph"),
    path('workflow/', views.workflow, name="workflow"),
    path('formulaeditor/', views.formulaeditor, name="formulaeditor"),
    path("pf/<int:custid>/<int:pfid>/<int:version>", views.procflow_detail, name="procflow_detail"),
    path("bc/<int:custid>/<int:bcid>/<int:version>", views.bc_detail, name="bc_detail"),
    path('q/<int:question_id>/', views.question_detail, name='question_detail'),
    

]
