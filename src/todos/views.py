import json
from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .models import ToDo
from .forms import ToDoForm
from logging import getLogger

logger = getLogger('todos')

@login_required
@require_http_methods(['GET', 'POST'])
def todo_list(request):
    logger.info(f"Todo list accessed by user: {request.user.username}")
    
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            
            logger.info(f"Todo created - ID: {todo.id}, Title: {todo.title}, User: {request.user.username}")

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
        else:
            logger.warning(f"Todo creation failed - User: {request.user.username}, Errors: {form.errors}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
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
    logger.debug(f"Todo detail accessed - Todo ID: {todo_id}, User: {request.user.username}")
    
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)

    if request.method == 'GET':
        context = {'todo':todo}
        return render(request, 'todos/todo_detail.html', context)
    elif request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            logger.info(f"Todo updated - ID: {todo.id}, User: {request.user.username}")

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
        else:
            logger.warning(f"Todo update failed - ID: {todo.id}, User: {request.user.username}, Errors: {form.errors}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success' : False,
                    'errors' : form.errors,
                }, status = 400)
    elif request.method == 'DELETE':
        logger.info(f"Todo deleted - ID: {todo.id}, Title: {todo.title}, User: {request.user.username}")
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
    
    logger.info(f"Todo completed - ID: {todo.id}, User: {request.user.username}")

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success' : True})
    return redirect('todos:todo_list')

@login_required
@require_http_methods(["POST"])
def todo_uncomplete(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.completed = False
    todo.save()
    
    logger.info(f"Todo uncompleted - ID: {todo.id}, User: {request.user.username}")

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success':True})
    return redirect('todos:todo_list')