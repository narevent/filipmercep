from django.db import models
from django.utils import timezone


class AboutPage(models.Model):
    """CMS-editable About Page content"""
    title = models.CharField(max_length=200, default="About Filip Merčep")
    subtitle = models.CharField(max_length=300, blank=True)
    intro_text = models.TextField(help_text="Main introduction paragraph")
    biography = models.TextField(help_text="Detailed biography")
    philosophy_quote = models.TextField(blank=True, help_text="Optional quote for philosophy section")
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "About Page Content"
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    @classmethod
    def get_content(cls):
        """Get or create about page content"""
        content, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'About Filip Merčep',
                'subtitle': 'Percussion Artist & Innovator',
                'intro_text': 'Filip Merčep is a renowned Croatian percussion artist.',
                'biography': 'Add detailed biography here.',
            }
        )
        return content


class Award(models.Model):
    """Awards and recognitions"""
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    class Meta:
        ordering = ['-year', 'order']


class Education(models.Model):
    """Educational background"""
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    year_start = models.IntegerField(blank=True, null=True)
    year_end = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
    class Meta:
        verbose_name_plural = "Education"
        ordering = ['order', '-year_end']


class Ensemble(models.Model):
    """Current and past ensemble memberships"""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']


class Concert(models.Model):
    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    ticket_link = models.URLField(blank=True)
    is_past = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.venue}"

    class Meta:
        ordering = ['-date']


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    external_link = models.URLField(blank=True)
    youtube_embed = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="YouTube video ID only (e.g., 'dQw4w9WgXcQ' from youtube.com/watch?v=dQw4w9WgXcQ)"
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-created_at']


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    external_link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-submitted_at']