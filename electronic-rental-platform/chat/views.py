from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Conversation, Message
from users.models import User
from .forms import MessageForm

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related('participants', 'messages')
    
    conversations_data = []
    for conv in conversations:
        other_user = conv.get_other_user(request.user)
        last_msg = conv.last_message()
        unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        
        conversations_data.append({
            'conversation': conv,
            'other_user': other_user,
            'last_message': last_msg,
            'unread_count': unread_count,
        })
    
    return render(request, 'chat/inbox.html', {'conversations_data': conversations_data})

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    
    if request.user not in conversation.participants.all():
        messages.error(request, 'You do not have access to this conversation.')
        return redirect('chat:inbox')
    
    other_user = conversation.get_other_user(request.user)
    
    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.updated_at = message.created_at
            conversation.save()
            return redirect('chat:conversation', pk=pk)
    else:
        form = MessageForm()
    
    messages_list = conversation.messages.all().select_related('sender')
    
    return render(request, 'chat/conversation.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages': messages_list,
        'form': form,
    })

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    
    if other_user == request.user:
        messages.error(request, 'You cannot message yourself.')
        return redirect('chat:inbox')
    
    # Check if conversation already exists
    existing_conv = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if existing_conv:
        return redirect('chat:conversation', pk=existing_conv.pk)
    
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    
    messages.success(request, f'Conversation started with {other_user.username}')
    return redirect('chat:conversation', pk=conversation.pk)

@login_required
def delete_conversation(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    
    if request.user not in conversation.participants.all():
        messages.error(request, 'You do not have access to this conversation.')
        return redirect('chat:inbox')
    
    if request.method == 'POST':
        conversation.delete()
        messages.success(request, 'Conversation deleted.')
        return redirect('chat:inbox')
    
    return render(request, 'chat/delete.html', {'conversation': conversation})
