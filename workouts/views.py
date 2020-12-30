from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, Member, Workout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import WorkoutForm, MemberForm
from blog.models import Blog

# Create your views here.
def index(request):
    recent_blogs = Blog.objects.order_by('-timestamp')[:3]
    context = {
        'recent_blogs':recent_blogs
    }
    return render(request, 'index.html', context)

def BodyBuilding(request):
    BodyBuildingExercise = Exercise.objects.filter(category__category="Body Building")
    context = {
        'BodyBuildingExercise':BodyBuildingExercise
    }
    return render(request, 'bodybuilding.html', context)

def Aerobic(request):
    AerobicExercise = Exercise.objects.filter(category__category="Aerobic")
    context = {
        'AerobicExercise':AerobicExercise
    }
    return render(request, 'aerobic.html', context)


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    context = {
        'exercise':exercise
    }
    return render(request, 'exercise_detail.html', context)

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Member.objects.create(user=user)
            return redirect('login')

    context = {
        'form':form
    }
    return render(request, 'register.html', context)

def loginPage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


def member(request):
    member = Member.objects.get(user=request.user)
    workouts = member.workout_set.all()
    total_workouts = workouts.count()
    in_progres = workouts.filter(status="In progress").count()
    finished = workouts.filter(status="Finished").count()
    form = MemberForm(instance=member)
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
    context = {
        'member':member,
        'workouts':workouts,
        'total_workouts':total_workouts,
        'in_progres':in_progres,
        'finished':finished,
        'form':form
    }
    return render(request, 'member.html', context)


def createWorkout(request):
    member = Member.objects.get(user=request.user)
    form = WorkoutForm(request.user)
    if request.method == "POST":
        form = WorkoutForm(request.user, request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('/')

    context = {
        'form':form
    }
    return render(request, 'workout_form.html', context)

def updateWorkout(request, id):
    workout = Workout.objects.get(id=id)
    form = WorkoutForm(request.user, instance=workout)

    if request.method == "POST":
        form = WorkoutForm(request.user, request.POST, instance=workout)

        if form.is_valid():
            form.instance.workout = workout
            form.save()
            return redirect('/')

    context = {
            'form':form
    }
    return render(request, 'workout_form.html', context)


def program(request):
    return render(request, 'program.html')

def about(request):
    return render(request, 'about.html')
