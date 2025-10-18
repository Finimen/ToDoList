import json
from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .models import ToDo
from .forms import ToDoForm

@login_required
@require_http_methods(['GET', 'POST'])
def todo_list(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success':True,
                    'todo':{
                        'id':todo.id,
                        'title':todo.title,
                        'content':todo.content,
                        'priority':todo.priority,
                        'due_date':todo.due_date.isoformat() if todo.due_date else None,
                        'completed':todo.completed,
                        'days_until_due':todo.days_until_due,
                    }
                }) 
            return redirect('todos:todo_list')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success':False,
                'errors':form.errors,
                }, status=400)
        
    todos = ToDo.objects.filter(user=request.user)
    form = ToDoForm()

    context = {
        'todos' : todos,
        'form' : form,
    }

    return render(request, 'todos/todo_list.html', context)

@login_required
@require_http_methods(["GET", "POST", "DELETE"])
def todo_detail(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)

    if request.method == 'GET':
        context = {'todo':todo}
        return render(request, 'todos/todo_detail.html', context)
    elif request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success' : True,
                    'todo' : {
                        'id' : todo.id,
                        'title' : todo.title,
                        'content' : todo.content,
                        'priority' : todo.priority,
                        'due_date' : todo.due_date.isoformat() if todo.due_date else None,
                        'completed' : todo.completed,
                        'days_until_due' : todo.days_until_due,
                    }
                })
            return redirect('todos:todo_list')
        elif  request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success' : False,
                'errors' : form.errors,
            }, status = 400)
    elif request.method == 'DELETE':
        todo.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success' : True})
    return redirect('todos:todo_list')
    
@login_required
@require_http_methods(["POST"])
def todo_complete(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.completed = True
    todo.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success' : True})
    return redirect('todos:todo_list')

@login_required
@require_http_methods(["POST"])
def todo_uncomplete(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.completed = False
    todo.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success':True})
    return redirect('todos:todo_list')