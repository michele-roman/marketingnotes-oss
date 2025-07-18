from django.db import models

class Chat(models.Model):
    chat_name = models.CharField(max_length=200)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_name

class Message(models.Model):
    SENDER_CHOICES = [
        ("user", "User"),
        ("chatbot", "Chatbot"),
    ]
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)

    def __str__(self):
        return f"Message from {self.sender} at {self.date}"

class MessageOpenAI(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='openai_responses')
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"OpenAI response at {self.date}"

class MessageGemini(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='gemini_responses')
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"Gemini response at {self.date}"

class MessageAntropic(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='antropic_responses')
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"Antropic response at {self.date}"

class MessageCustom(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='custom_responses')
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"Custom response at {self.date}"

class SuggestedMessage(models.Model):
    """Model for storing suggested messages that users can quickly send"""
    content = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content[:50]}..."

class APIKey(models.Model):
    """Model for storing API keys for different AI services"""
    SERVICE_CHOICES = [
        ('openai', 'OpenAI'),
        ('gemini', 'Google Gemini'),
        ('anthropic', 'Anthropic Claude'),
    ]
    
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, unique=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_service_display()} API Key"

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

