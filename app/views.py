from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message, SuggestedMessage, MessageOpenAI, MessageGemini, MessageAntropic, MessageCustom
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
import json
import logging
from .models import APIKey

logger = logging.getLogger(__name__)

# Chat Views
class ChatListView(ListView):
    model = Chat
    template_name = 'chat/chat_detail.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.all().order_by('-creation_datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggested_messages'] = SuggestedMessage.objects.all()
        # Add all chats for the dropdown menu
        context['all_chats'] = Chat.objects.all().order_by('-creation_datetime')
        
        # If there are any chats, get the most recent one
        if self.get_queryset().exists():
            context['chat'] = self.get_queryset().first()
            context['messages'] = context['chat'].message_set.all().order_by('date')
        else:
            # If no chats exist, create a new one
            chat = Chat.objects.create(
                chat_name="New Chat"
            )
            context['chat'] = chat
            context['messages'] = []
            
        return context

class ChatDetailView(DetailView):
    model = Chat
    template_name = 'chat/chat_detail.html'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.message_set.all().order_by('date')
        context['suggested_messages'] = SuggestedMessage.objects.all()
        # Add all chats for the dropdown menu
        context['all_chats'] = Chat.objects.all().order_by('-creation_datetime')
        return context

class ChatCreateView(CreateView):
    model = Chat
    fields = []
    template_name = 'chat/chat_detail.html'

    def get(self, request, *args, **kwargs):
        # Create new chat directly
        chat = Chat.objects.create(
            chat_name="New Chat"
        )
        # Redirect to the chat list page which will show the chat detail
        return redirect('chat-list')

    def form_valid(self, form):
        form.instance.chat_name = "New Chat"
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chat-list')

class ChatUpdateView(SuccessMessageMixin, UpdateView):
    model = Chat
    fields = ['chat_name']
    template_name = 'chat/chat_detail.html'
    success_message = "Chat name was updated successfully"

    def get_success_url(self):
        return reverse_lazy('chat-detail', kwargs={'pk': self.object.pk})

@require_POST
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'})
    
    # Create user message
    user_message = Message.objects.create(
        chat=chat,
        content=content,
        sender='user'
    )
    
    # Get responses from all agents
    from .agent import get_openai_agent, get_gemini_agent, get_antropic_agent, get_custom_agent
    
    responses = {}
    
    # OpenAI response
    try:
        openai_agent = get_openai_agent(chat_id=chat_id)
        openai_response = openai_agent(content)
        
        openai_message = MessageOpenAI.objects.create(
            chat=chat,
            content=openai_response,
            user_message=user_message
        )
        responses['openai'] = {
            'id': openai_message.id,
            'content': openai_message.content,
            'date': openai_message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        logger.error(f"Error getting OpenAI response: {str(e)}")
        openai_response = "Sorry, I'm having trouble responding right now. Please try again."
        openai_message = MessageOpenAI.objects.create(
            chat=chat,
            content=openai_response,
            user_message=user_message
        )
        responses['openai'] = {
            'id': openai_message.id,
            'content': openai_message.content,
            'date': openai_message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    # Gemini response
    try:
        gemini_agent = get_gemini_agent(chat_id=chat_id)
        gemini_response = gemini_agent(content)
        
        gemini_message = MessageGemini.objects.create(
            chat=chat,
            content=gemini_response,
            user_message=user_message
        )
        responses['gemini'] = {
            'id': gemini_message.id,
            'content': gemini_message.content,
            'date': gemini_message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        logger.error(f"Error getting Gemini response: {str(e)}")
        gemini_response = "Sorry, I'm having trouble responding right now. Please try again."
        gemini_message = MessageGemini.objects.create(
            chat=chat,
            content=gemini_response,
            user_message=user_message
        )
        responses['gemini'] = {
            'id': gemini_message.id,
            'content': gemini_message.content,
            'date': gemini_message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    # Antropic response
    try:
        anthropic_agent = get_antropic_agent(chat_id=chat_id)
        anthropic_response = anthropic_agent(content)
        
        anthropic_message = MessageAntropic.objects.create(
            chat=chat,
            content=anthropic_response,
            user_message=user_message
        )
        responses['antropic'] = {
            'id': anthropic_message.id,
            'content': anthropic_message.content,
            'date': anthropic_message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        logger.error(f"Error getting Antropic response: {str(e)}")
        anthropic_response = "Sorry, I'm having trouble responding right now. Please try again."
        anthropic_message = MessageAntropic.objects.create(
            chat=chat,
            content=anthropic_response,
            user_message=user_message
        )
        responses['antropic'] = {
            'id': anthropic_message.id,
            'content': anthropic_message.content,
            'date': anthropic_message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    # Custom response
    try:
        custom_agent = get_custom_agent(chat_id=chat_id)
        custom_response = custom_agent(content)
        
        custom_message = MessageCustom.objects.create(
            chat=chat,
            content=custom_response,
            user_message=user_message
        )
        responses['custom'] = {
            'id': custom_message.id,
            'content': custom_message.content,
            'date': custom_message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        logger.error(f"Error getting Custom response: {str(e)}")
        custom_response = "Sorry, I'm having trouble responding right now. Please try again."
        custom_message = MessageCustom.objects.create(
            chat=chat,
            content=custom_response,
            user_message=user_message
        )
        responses['custom'] = {
            'id': custom_message.id,
            'content': custom_message.content,
            'date': custom_message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    return JsonResponse({
        'status': 'success',
        'user_message': {
            'content': user_message.content,
            'date': user_message.date.strftime('%Y-%m-%d %H:%M:%S')
        },
        'responses': responses
    })

@require_POST
def select_ai_response(request, chat_id):
    """Select which AI response to continue the conversation with"""
    response_id = request.POST.get('response_id')
    ai_type = request.POST.get('ai_type')  # 'openai', 'gemini', 'antropic', or 'custom'
    
    if not response_id or not ai_type:
        return JsonResponse({'status': 'error', 'message': 'Missing response_id or ai_type'})
    
    try:
        if ai_type == 'openai':
            ai_response = MessageOpenAI.objects.get(id=response_id, chat_id=chat_id)
        elif ai_type == 'gemini':
            ai_response = MessageGemini.objects.get(id=response_id, chat_id=chat_id)
        elif ai_type == 'antropic':
            ai_response = MessageAntropic.objects.get(id=response_id, chat_id=chat_id)
        elif ai_type == 'custom':
            ai_response = MessageCustom.objects.get(id=response_id, chat_id=chat_id)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid AI type'})
        
        # Mark as selected
        ai_response.is_selected = True
        ai_response.save()
        
        # Create a regular chatbot message in the main conversation
        agent_message = Message.objects.create(
            chat_id=chat_id,
            content=ai_response.content,
            sender='chatbot'
        )
        
        return JsonResponse({
            'status': 'success',
            'agent_message': {
                'content': agent_message.content,
                'date': agent_message.date.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except (MessageOpenAI.DoesNotExist, MessageGemini.DoesNotExist, MessageAntropic.DoesNotExist, MessageCustom.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Response not found'})
    except Exception as e:
        logger.error(f"Error selecting AI response: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error selecting response'})

@require_POST
def add_text_to_custom(request, chat_id):
    """Add selected text from other AI responses to the custom editor"""
    selected_text = request.POST.get('selected_text', '').strip()
    
    if not selected_text:
        return JsonResponse({'status': 'error', 'message': 'No text selected'})
    
    try:
        # Get the current custom response for this chat
        custom_response = MessageCustom.objects.filter(chat_id=chat_id).order_by('-date').first()
        
        if custom_response:
            # Append the selected text to existing content
            new_content = custom_response.content + "\n\n" + selected_text
            custom_response.content = new_content
            custom_response.save()
        else:
            # Create a new custom response
            custom_response = MessageCustom.objects.create(
                chat_id=chat_id,
                content=selected_text
            )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Text added to custom response',
            'custom_content': custom_response.content
        })
        
    except Exception as e:
        logger.error(f"Error adding text to custom: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error adding text to custom response'})

@require_POST
def update_custom_response(request, chat_id):
    """Update the custom response with manually typed content"""
    custom_content = request.POST.get('custom_content', '').strip()
    
    if not custom_content:
        return JsonResponse({'status': 'error', 'message': 'Custom content cannot be empty'})
    
    try:
        # Get the current custom response for this chat
        custom_response = MessageCustom.objects.filter(chat_id=chat_id).order_by('-date').first()
        
        if custom_response:
            # Update existing content
            custom_response.content = custom_content
            custom_response.save()
        else:
            # Create a new custom response
            custom_response = MessageCustom.objects.create(
                chat_id=chat_id,
                content=custom_content
            )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Custom response updated',
            'custom_content': custom_response.content
        })
        
    except Exception as e:
        logger.error(f"Error updating custom response: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error updating custom response'})

def home(request):
    """Home view that redirects to chat list"""
    return redirect('chat-list')

class APIKeysView(View):
    """View for managing API keys"""
    template_name = 'api_keys.html'
    
    def get(self, request):
        # Get or create API key objects for each service
        openai_key, _ = APIKey.objects.get_or_create(service='openai')
        gemini_key, _ = APIKey.objects.get_or_create(service='gemini')
        anthropic_key, _ = APIKey.objects.get_or_create(service='anthropic')
        
        context = {
            'openai_key': openai_key,
            'gemini_key': gemini_key,
            'anthropic_key': anthropic_key,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        # Handle API key updates
        openai_key = request.POST.get('openai_key', '').strip()
        gemini_key = request.POST.get('gemini_key', '').strip()
        anthropic_key = request.POST.get('anthropic_key', '').strip()
        
        # Update OpenAI key
        openai_obj, _ = APIKey.objects.get_or_create(service='openai')
        openai_obj.api_key = openai_key
        openai_obj.is_active = bool(openai_key)
        openai_obj.save()
        
        # Update Gemini key
        gemini_obj, _ = APIKey.objects.get_or_create(service='gemini')
        gemini_obj.api_key = gemini_key
        gemini_obj.is_active = bool(gemini_key)
        gemini_obj.save()
        
        # Update Anthropic key
        anthropic_obj, _ = APIKey.objects.get_or_create(service='anthropic')
        anthropic_obj.api_key = anthropic_key
        anthropic_obj.is_active = bool(anthropic_key)
        anthropic_obj.save()
        
        messages.success(request, 'API keys updated successfully!')
        return redirect('api-keys')
