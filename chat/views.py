from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Message
from users.models import User
import urllib.parse

@login_required
def chat_page(request):
    employees = User.objects.filter(role='employee')
    manager = request.user
    unread_counts = {}

    for employee in employees:
        unread_count = Message.objects.filter(
            sender=employee,
            receiver=manager,
            is_read=False
        ).count()
        unread_counts[employee.email] = unread_count

    return render(request, 'chat/chat.html', {
        'employees': employees,
        'unread_counts': unread_counts
    })
@login_required
def employee_chat_page(request):
    user_email = request.user.email
    if not user_email:
        return render(request, 'chat/employee_chat.html', {
            'room_name': '',
            'manager_email': '',
            'error': 'User email is not available. Please log in again.'
        })
    try:
        manager = User.objects.get(role='manager')
        manager_email = manager.email
        if user_email == manager_email:
            return render(request, 'chat/employee_chat.html', {
                'room_name': '',
                'manager_email': '',
                'error': 'Cannot chat with yourself. Please contact support.'
            })
        room_name = f"{min(user_email, manager_email)}__{max(user_email, manager_email)}"
        print("Employee chat - room_name:", room_name, "manager_email:", manager_email)  # للتصحيح
    except User.DoesNotExist:
        return render(request, 'chat/employee_chat.html', {
            'room_name': '',
            'manager_email': '',
            'error': 'No manager found. Please contact support.'
        })
    return render(request, 'chat/employee_chat.html', {
        'room_name': room_name,
        'manager_email': manager_email,
        'user_email': user_email

    })

@login_required
def manager_private_chat(request, email):
    employee = get_object_or_404(User, email=email)
    room_name = f"{min(request.user.email, email)}__{max(request.user.email, email)}"
    print("Manager private chat - room_name:", room_name, "employee_email:", email)  # للتصحيح
    return render(request, 'chat/chat.html', {
        'employee': employee,
        'room_name': room_name, 
        'user_email': request.user.email

        
    })

@login_required
def message_list(request):
    import urllib.parse
    room_name = urllib.parse.unquote(request.GET.get('room', ''))

    if not room_name or '__' not in room_name:
        return JsonResponse({'error': 'Invalid room name'}, status=400)

    try:
        parts = room_name.split('__')
        if len(parts) != 2:
            return JsonResponse({'error': 'Room name format must be two emails separated by double underscore'}, status=400)

        email1, email2 = parts

        if not email1 or not email2:
            return JsonResponse({'error': 'Invalid email format in room name'}, status=400)

        user1 = User.objects.get(email=email1)
        user2 = User.objects.get(email=email2)

        messages = Message.objects.filter(
            sender__in=[user1, user2],
            receiver__in=[user1, user2, None]
        ).order_by('timestamp')

        data = [{
            'sender': msg.sender.email,
            'message': msg.content,
            'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'is_read': msg.is_read
        } for msg in messages]

        return JsonResponse(data, safe=False)

    except User.DoesNotExist:
        return JsonResponse({'error': 'One or both users not found'}, status=404)
    except Exception as e:
        print("Error in message_list:", str(e))  # للتصحيح
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def mark_read(request):
    from_email = request.GET.get('email')
    if not from_email:
        return JsonResponse({'error': 'No email provided'}, status=400)

    try:
        sender = User.objects.get(email=from_email)
        receiver = request.user

        Message.objects.filter(sender=sender, receiver=receiver, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@login_required
def unread_counts(request):
    print(f"User: {request.user}, Role: {request.user.role}, Authenticated: {request.user.is_authenticated}")
    if not request.user.is_authenticated or request.user.role.lower() != 'manager':
        print(f"Access denied for user {request.user.email}: Role is {request.user.role}")
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    unread_counts = {}
    employees = User.objects.filter(role='employee')
    for employee in employees:
        count = Message.objects.filter(
            sender=employee,
            receiver=request.user,
            is_read=False
        ).count()
        unread_counts[employee.email] = count
    print(f"Returning unread counts: {unread_counts}")
    return JsonResponse(unread_counts)