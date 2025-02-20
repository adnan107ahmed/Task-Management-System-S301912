from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task

def home(request, project_id=None):
    # If a project_id is passed in the URL, filter tasks by that project
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        tasks = Task.objects.filter(project=project)
    else:
        # If no project_id is provided, show all tasks
        tasks = Task.objects.all()

    projects = Project.objects.all()  # Get all projects to populate the dropdown

    return render(request, 'home.html', {'tasks': tasks, 'projects': projects, 'selected_project_id': project_id})

def create_project(request):
    if request.method == 'POST':
        name = request.POST['name']

        Project.objects.create(
            name=name,
        )

    return render(request, 'create_project.html')

def create_or_update_task(request, task_id=None):
    if task_id:  
        task = get_object_or_404(Task, id=task_id)
    else:  
        task = None

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        project_id = request.POST.get('project')

        project = get_object_or_404(Project, id=project_id)

        if task:  
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
    task = get_object_or_404(Task, id=task_id)  
    task.delete()
    return redirect('home')