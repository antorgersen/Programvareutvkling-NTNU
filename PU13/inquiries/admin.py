from django.contrib import admin
from .models import Inquiries

class MessagesAdmin(admin.ModelAdmin):
    list_display = ('text_from', 'created_at','subject', 'description')

admin.site.register(Inquiries, MessagesAdmin)