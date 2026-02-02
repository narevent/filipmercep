from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from .models import (
    Concert, Project, NewsItem, NewsletterSubscriber, 
    ContactMessage, AboutPage, Award, Education, Ensemble
)
from .forms import NewsletterForm, ContactForm


def home(request):
    """Homepage with featured news and recent updates"""
    featured_news = NewsItem.objects.filter(is_featured=True).first()
    recent_news = NewsItem.objects.all()[:3]
    upcoming_concerts = Concert.objects.filter(is_past=False)[:3]
    
    # Newsletter subscription - Fixed to fail silently
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            try:
                # Save to database
                subscriber = form.save()
                messages.success(request, 'Successfully subscribed to newsletter!')
                
                # Try to send confirmation email, but don't fail if it doesn't work
                try:
                    send_mail(
                        'Newsletter Subscription Confirmed',
                        f'Thank you for subscribing to Filip Merčep\'s newsletter!',
                        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@filipmercep.com',
                        [subscriber.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    # Email failed but subscription still succeeded
                    print(f"Email notification failed: {e}")
                    
            except IntegrityError:
                # Email already exists
                messages.error(request, 'This email is already subscribed.')
            except Exception as e:
                # Any other error
                messages.error(request, 'An error occurred. Please try again.')
                print(f"Newsletter subscription error: {e}")
            
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'featured_news': featured_news,
        'recent_news': recent_news,
        'upcoming_concerts': upcoming_concerts,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'website/home.html', context)


def about(request):
    """About page with CMS content"""
    about_content = AboutPage.get_content()
    awards = Award.objects.all()
    education = Education.objects.all()
    ensembles = Ensemble.objects.filter(is_current=True)
    
    context = {
        'about': about_content,
        'awards': awards,
        'education': education,
        'ensembles': ensembles,
    }
    return render(request, 'website/about.html', context)


def concerts(request):
    """Concerts page with upcoming and past concerts"""
    upcoming = Concert.objects.filter(is_past=False)
    past = Concert.objects.filter(is_past=True)[:10]
    
    context = {
        'upcoming_concerts': upcoming,
        'past_concerts': past,
    }
    return render(request, 'website/concerts.html', context)


def projects(request):
    """Projects showcase page"""
    all_projects = Project.objects.all()
    
    context = {
        'projects': all_projects,
    }
    return render(request, 'website/projects.html', context)


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Try to send email notification, but don't fail if email isn't configured
            try:
                send_mail(
                    f'New Contact Form: {contact_message.subject}',
                    f'From: {contact_message.name} ({contact_message.email})\n\n{contact_message.message}',
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@filipmercep.com',
                    ['info@filipmercep.com'],
                    fail_silently=True,
                )
            except Exception as e:
                # Email failed but message is still saved in database
                print(f"Email notification failed: {e}")
            
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'website/contact.html', context)