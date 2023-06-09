from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #Las contraseñas son iguales entra
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "Error": 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "Error": 'Las contraseñas no coinciden'
                })

        print(request.POST)
        print('Recibiendo datos')
    
    return render(request, 'signup.html', {
        'form': UserCreationForm
    })

def task(request):
    tasks = Task.objects.filter(user=request.user, finaliza__isnull=True)
    return render(request, 'task.html', {'tasks' : tasks})

def task_completed(request):
    tasks = Task.objects.filter(user=request.user, finaliza__isnull=False)
    return render(request, 'task.html', {'tasks' : tasks})

def cerrarsesion(request):
    logout(request)
    return redirect('home')

def singin(request):
    if request.method == 'GET':   
        return render(request, 'signin.html', {
            'form':AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'Error' : 'El nombre de usuario o la contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('task')

def create_task(request):


    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        form = TaskForm(request.POST)
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('task')
    
def task_detail(request, task_id): 
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('task')
    
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.finaliza = timezone.now()
        task.save()
        ##Corregir que elimine y no que guarde que esta finalizada
        return redirect('task')
    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')