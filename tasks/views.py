from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Project, Task  # Import models correctly
from .templates.forms import UserCreationForm, LoginForm

User = get_user_model()  # Get the custom User model from models.py
current_user = ''
# ----------------- USER AUTHENTICATION ----------------- #
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user data
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # Optionally, you can log errors for debugging
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            current_user = User.objects.get(username=username, password=password)
            if current_user is not None:
                login(request, current_user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")
# ----------------- TASK & PROJECT MANAGEMENT ----------------- #
@login_required
def home(request, project_id=None):
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        tasks = Task.objects.filter(project=project)
    else:
        tasks = Task.objects.all()

    projects = Project.objects.all()
    return render(request, 'home.html', {'tasks': tasks, 'projects': projects, 'selected_project_id': project_id})

def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'projects': projects})

def create_or_update_project(request, project_id=None):
    error = None
    project = None

    if project_id:
        project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        name = request.POST['name']
        try:
            if project:
                project.name = name
                project.save()
            else:
                Project.objects.create(name=name)

            return redirect('projects_list')
        except IntegrityError:
            error = "Project name must be unique. Please choose a different name."

    return render(request, 'create_project.html', {'project': project, 'error': error})

def create_or_update_task(request, task_id=None):
    task = get_object_or_404(Task, id=task_id) if task_id else None
    if task and hasattr(request.user, 'role') and request.user.role == "user":
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        project_id = request.POST.get('project')

        project = get_object_or_404(Project, id=project_id)

        if hasattr(request.user, 'role') and request.user.role == "user" and task:
            task.title = title
            task.description = description
            task.due_date = due_date
            task.priority = priority
            task.status = status
            task.project = project
            task.save()
        else:
            Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status,
                project=project
            )
        return redirect('home')

    return render(request, 'task_form.html', {'task': task, 'projects': Project.objects.all()})

def delete_task(request, task_id):
    if request.user == "admin":
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('home')

def delete_project(request, project_id):
    if request.user == "admin":
        project = get_object_or_404(Project, id=project_id)
        project.delete()
    return redirect('projects_list')
