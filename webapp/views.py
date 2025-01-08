from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from .models import Record

# Homepage
def home(request):
    return render(request, "webapp/index.html")


# Register a user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return HttpResponseRedirect(reverse('webapp:login'))

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)


# Login a user
def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have logged!")
                return HttpResponseRedirect(reverse("webapp:dashboard"))

    context = {'form':form}

    return render(request, 'webapp/mylogin.html', context=context)


# Dashboard
@login_required(login_url="webapp:login")
def dashboard(request):
    records = Record.objects.all()
    context = {'records':records}

    return render(request, 'webapp/dashboard.html', context=context)

# Create a record
@login_required(login_url="webapp:login")
def create_record(request):
    form = CreateRecordForm()

    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was created!")
            return HttpResponseRedirect(reverse("webapp:dashboard"))

    context = {'form':form}

    return render(request, 'webapp/create-record.html', context=context)


# Update a record
@login_required(login_url="webapp:login")
def update_record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)
    form = UpdateRecordForm(instance=record)

    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return HttpResponseRedirect(reverse("webapp:record", args=(record_id,)))

    context = {'form':form, 'id':record_id}

    return render(request, 'webapp/update-record.html', context=context)


# Read a record
@login_required(login_url="webapp:login")
def singular_record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)

    context = {'record':record}

    return render(request, 'webapp/view-record.html', context=context)


# Delete a record
@login_required(login_url="webapp:login")
def delete_record(request, record_id):
    record = Record.objects.get(pk=record_id).delete()

    messages.success(request, "Your record was deleted!")

    return HttpResponseRedirect(reverse("webapp:dashboard"))


# User logout
def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logout success!")
    return HttpResponseRedirect(reverse("webapp:home"))
