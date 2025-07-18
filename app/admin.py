from django.contrib import admin
from .models import Chat, Message, MessageOpenAI, MessageGemini, MessageAntropic, MessageCustom, APIKey

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_name', 'creation_datetime')
    list_filter = ('creation_datetime',)
    search_fields = ('chat_name',)
    ordering = ('-creation_datetime',)
    readonly_fields = ('creation_datetime',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'content', 'date')
    list_filter = ('sender', 'date', 'chat')
    search_fields = ('content', 'chat__chat_name')
    ordering = ('-date',)
    readonly_fields = ('date',)
    list_select_related = ('chat',)

@admin.register(MessageOpenAI)
class MessageOpenAIAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user_message', 'is_selected', 'date')
    list_filter = ('is_selected', 'date', 'chat')
    search_fields = ('content', 'chat__chat_name', 'user_message__content')
    ordering = ('-date',)
    readonly_fields = ('date',)
    list_select_related = ('chat', 'user_message')
    actions = ['mark_as_selected', 'mark_as_not_selected']

    def mark_as_selected(self, request, queryset):
        queryset.update(is_selected=True)
    mark_as_selected.short_description = "Mark selected responses as selected"

    def mark_as_not_selected(self, request, queryset):
        queryset.update(is_selected=False)
    mark_as_not_selected.short_description = "Mark selected responses as not selected"

@admin.register(MessageGemini)
class MessageGeminiAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user_message', 'is_selected', 'date')
    list_filter = ('is_selected', 'date', 'chat')
    search_fields = ('content', 'chat__chat_name', 'user_message__content')
    ordering = ('-date',)
    readonly_fields = ('date',)
    list_select_related = ('chat', 'user_message')
    actions = ['mark_as_selected', 'mark_as_not_selected']

    def mark_as_selected(self, request, queryset):
        queryset.update(is_selected=True)
    mark_as_selected.short_description = "Mark selected responses as selected"

    def mark_as_not_selected(self, request, queryset):
        queryset.update(is_selected=False)
    mark_as_not_selected.short_description = "Mark selected responses as not selected"

@admin.register(MessageAntropic)
class MessageAntropicAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user_message', 'is_selected', 'date')
    list_filter = ('is_selected', 'date', 'chat')
    search_fields = ('content', 'chat__chat_name', 'user_message__content')
    ordering = ('-date',)
    readonly_fields = ('date',)
    list_select_related = ('chat', 'user_message')
    actions = ['mark_as_selected', 'mark_as_not_selected']

    def mark_as_selected(self, request, queryset):
        queryset.update(is_selected=True)
    mark_as_selected.short_description = "Mark selected responses as selected"

    def mark_as_not_selected(self, request, queryset):
        queryset.update(is_selected=False)
    mark_as_not_selected.short_description = "Mark selected responses as not selected"

@admin.register(MessageCustom)
class MessageCustomAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user_message', 'is_selected', 'date')
    list_filter = ('is_selected', 'date', 'chat')
    search_fields = ('content', 'chat__chat_name', 'user_message__content')
    ordering = ('-date',)
    readonly_fields = ('date',)
    list_select_related = ('chat', 'user_message')
    actions = ['mark_as_selected', 'mark_as_not_selected']

    def mark_as_selected(self, request, queryset):
        queryset.update(is_selected=True)
    mark_as_selected.short_description = "Mark selected responses as selected"

    def mark_as_not_selected(self, request, queryset):
        queryset.update(is_selected=False)
    mark_as_not_selected.short_description = "Mark selected responses as not selected"

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('service', 'is_active', 'created_at', 'updated_at')
    list_filter = ('service', 'is_active', 'created_at', 'updated_at')
    search_fields = ('service',)
    ordering = ('service',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('service', 'api_key', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('service',)
        return self.readonly_fields
