# chat/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Message, User
from django.views.decorators.csrf import csrf_exempt
import json

def chat_page(request):
    users = User.objects.exclude(id=request.user.id)  # all other users
    return render(request, 'admin_chat.html', {'users': users})

def get_messages(request, user_id):
    messages = Message.objects.filter(
        sender_id__in=[request.user.id, user_id],
        receiver_id__in=[request.user.id, user_id]
    ).order_by('timestamp')

    return JsonResponse([
        {
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for msg in messages
    ], safe=False)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from django.contrib.auth.models import User

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        sender = request.user
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Receiver does not exist'}, status=400)

        message = Message.objects.create(sender=sender, receiver=receiver, content=content)
        return JsonResponse({'status': 'Message sent', 'message_id': message.id})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
