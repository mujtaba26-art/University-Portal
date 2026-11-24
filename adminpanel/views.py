from django.shortcuts import render
from .models import *
from .forms import *
# views.py
from django.shortcuts import render, redirect
from .forms import *

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

def create_user_view(request):
    if request.method == 'POST':
        form = CustomUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Replace with your success URL
    else:
        form = CustomUser()
    
    return render(request, 'admin/createuser.html', {'form': form})

# Create your views here.
def adminpanel(request):
    return render(request,'admin/home.html')

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'admin/user.html', {'users': users})

# views.py
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = CustomUser(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')  # Change this to your success URL
    else:
        form = CustomUser(instance=user)

    return render(request, 'admin/edit_user.html', {'form': form, 'user': user})

def teachersdocumentviews(request,user,subject):
    return render(request,'admin/teacherdocument.html')



# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from django.contrib.auth.models import User

@csrf_exempt
def get_messages(request):
    if request.method == "POST":
        teacher_id = request.POST.get("teacher_id")
        messages = Message.objects.filter(sender_id=teacher_id) | Message.objects.filter(receiver_id=teacher_id)
        messages = messages.order_by("timestamp")
        data = [
            {
                "sender": msg.sender.username,
                "content": msg.content,
                "is_admin": msg.sender.is_superuser
            } for msg in messages
        ]
        return JsonResponse({"messages": data})

@csrf_exempt
def send_message(request):
    if request.method == "POST":
        sender_id = request.user.id
        receiver_id = request.POST.get("receiver_id")
        content = request.POST.get("content")
        Message.objects.create(sender_id=sender_id, receiver_id=receiver_id, content=content)
        return JsonResponse({"status": "Message sent"})
