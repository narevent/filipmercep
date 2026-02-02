from django.contrib import admin
from .models import (
    AboutPage, Award, Education, Ensemble,
    NewsletterSubscriber, Concert, Project, NewsItem, ContactMessage
)


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """Single About Page - only one instance exists"""
    list_display = ['title', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one About Page
        return not AboutPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of About Page
        return False


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'order']
    list_editable = ['order']
    list_filter = ['year']
    search_fields = ['title', 'description']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'year_start', 'year_end', 'order']
    list_editable = ['order']
    search_fields = ['institution', 'degree']


@admin.register(Ensemble)
class EnsembleAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_current', 'order']
    list_editable = ['order']
    list_filter = ['is_current']
    search_fields = ['name', 'role']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    date_hierarchy = 'subscribed_at'
    actions = ['export_emails']
    
    def export_emails(self, request, queryset):
        """Export email addresses"""
        emails = ', '.join([sub.email for sub in queryset])
        self.message_user(request, f"Emails: {emails}")
    export_emails.short_description = "Export selected email addresses"


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['title', 'venue', 'city', 'date', 'is_past']
    list_filter = ['is_past', 'date', 'city']
    search_fields = ['title', 'venue', 'city']
    date_hierarchy = 'date'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'has_youtube', 'has_image', 'created_at']
    list_editable = ['order']
    search_fields = ['title', 'description']
    
    def has_youtube(self, obj):
        return bool(obj.youtube_embed)
    has_youtube.boolean = True
    has_youtube.short_description = 'YouTube'
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Image'


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'is_featured']
    list_filter = ['is_featured', 'published_date']
    search_fields = ['title', 'content']
    date_hierarchy = 'published_date'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'is_read']
    list_filter = ['is_read', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'submitted_at'
    readonly_fields = ['submitted_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} messages marked as unread.")
    mark_as_unread.short_description = "Mark selected as unread"