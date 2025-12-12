from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date
from datetime import timedelta
from .models import LostItem, FoundItem, SuccessStory
from .forms import LostItemForm, FoundItemForm, SearchForm, SuccessStoryForm

def lostItems(request):
    items = LostItem.objects.filter(status="lost").order_by("-created_at")
    return render(request, "lost_items.html", {"lost_items": items})

def submit_success_story(request):
    if request.method == 'POST':
        form = SuccessStoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            # CHANGE THIS LINE: Set to True so stories show immediately
            story.is_published = True  # Changed from False to True
            story.save()
            messages.success(request, 'Thank you for sharing your story! It has been published.')
            return redirect('successStories')
        else:
            # If form is invalid, render the page again with errors
            return render_success_stories_page(request, form)
    else:
        # GET request - show empty form
        return render_success_stories_page(request, SuccessStoryForm())

def render_success_stories_page(request, form=None):
    """Helper function to render the success stories page with common context"""
    # Get all published stories ordered by creation date
    stories_list = SuccessStory.objects.filter(is_published=True).order_by("-created_at")
    
    # Pagination - 9 stories per page
    paginator = Paginator(stories_list, 9)
    page_number = request.GET.get('page')
    stories = paginator.get_page(page_number)
    
    # Get featured story (either marked as featured or the most recent)
    featured_story = stories_list.filter(is_featured=True).first()
    if not featured_story and stories_list:
        featured_story = stories_list.first()
    
    # Calculate statistics
    total_reunions = SuccessStory.objects.filter(is_published=True).count()
    
    # Calculate success rate based on lost/found items claimed
    total_lost_claimed = LostItem.objects.filter(status='claimed').count()
    total_lost = LostItem.objects.count()
    lost_success_rate = round((total_lost_claimed / total_lost * 100), 2) if total_lost > 0 else 0
    
    total_found_claimed = FoundItem.objects.filter(status='claimed').count()
    total_found = FoundItem.objects.count()
    found_success_rate = round((total_found_claimed / total_found * 100), 2) if total_found > 0 else 0
    
    # Overall success rate as average of both
    overall_success_rate = round((lost_success_rate + found_success_rate) / 2) if (lost_success_rate + found_success_rate) > 0 else 94
    
    # Calculate average recovery time (simplified - you might want more sophisticated logic)
    # Here we're using a placeholder value
    success_stories_with_dates = SuccessStory.objects.filter(
        is_published=True,
        created_at__isnull=False
    )[:10]  # Sample of recent stories
    
    avg_recovery_hours = 24  # Default value
    
    if success_stories_with_dates.exists():
        # This is a simplified calculation - you might have actual recovery time in your model
        avg_recovery_hours = 24  # Replace with actual calculation if you have the data
    
    context = {
        'stories': stories,
        'featured_story': featured_story,
        'total_reunions': total_reunions,
        'total_stories': total_reunions,
        'success_rate': overall_success_rate,
        'form': form if form else SuccessStoryForm(),
        'avg_recovery': avg_recovery_hours,
    }
    
    return render(request, "success_stories.html", context)

def home(request):
    form = SearchForm(request.GET or None)
    recent_lost = LostItem.objects.filter(status='lost').order_by("-created_at")[:3]
    recent_found = FoundItem.objects.filter(status='unclaimed').order_by("-created_at")[:3]
    
    # Get success stories for homepage display
    recent_success_stories = SuccessStory.objects.filter(is_published=True).order_by("-created_at")[:3]
    
    lost_results = None
    found_results = None

    if form.is_valid() and any(request.GET.values()):
        q = form.cleaned_data.get('search')
        cat = form.cleaned_data.get('category')
        loc = form.cleaned_data.get('location')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        lost_qs = LostItem.objects.filter(status='lost')
        found_qs = FoundItem.objects.filter(status='unclaimed')

        if q:
            lost_qs = lost_qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
            found_qs = found_qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if cat:
            lost_qs = lost_qs.filter(category=cat)
            found_qs = found_qs.filter(category=cat)
        if loc:
            lost_qs = lost_qs.filter(location__icontains=loc)
            found_qs = found_qs.filter(location__icontains=loc)
        if date_from:
            lost_qs = lost_qs.filter(date_lost__gte=date_from)
            found_qs = found_qs.filter(date_found__gte=date_from)
        if date_to:
            lost_qs = lost_qs.filter(date_lost__lte=date_to)
            found_qs = found_qs.filter(date_found__lte=date_to)

        lost_results = lost_qs.order_by('-created_at')
        found_results = found_qs.order_by('-created_at')
    
    # Calculate stats from database
    total_success_stories = SuccessStory.objects.filter(is_published=True).count()
    
    # Items reunited - multiply by a factor if you want to estimate
    items_reunited = total_success_stories * 10  # Assuming each story represents multiple items
    
    # Success rate calculation
    total_lost_claimed = LostItem.objects.filter(status='claimed').count()
    total_lost = LostItem.objects.count()
    lost_success_rate = (total_lost_claimed / total_lost * 100) if total_lost > 0 else 0
    
    total_found_claimed = FoundItem.objects.filter(status='claimed').count()
    total_found = FoundItem.objects.count()
    found_success_rate = (total_found_claimed / total_found * 100) if total_found > 0 else 0
    
    overall_success_rate = round((lost_success_rate + found_success_rate) / 2)
    
    # Calculate average recovery time (simplified)
    # You might want to add recovery_time field to your models for better accuracy
    recent_claimed = LostItem.objects.filter(status='claimed', updated_at__isnull=False).order_by('-updated_at')[:10]
    if recent_claimed.exists():
        # Simple average - you might have better logic
        avg_recovery = "24h"
    else:
        avg_recovery = "24h"

    stats = {
        "items_reunited": items_reunited,
        "success_rate": f"{overall_success_rate}%",
        "avg_recovery": avg_recovery,
        "total_stories": total_success_stories,
    }

    return render(request, "home.html", {
        "recent_lost": recent_lost,
        "recent_found": recent_found,
        "recent_success_stories": recent_success_stories,
        "stats": stats,
        "search_form": form,
    })

def search_results(request):
    form = SearchForm(request.GET or None)
    lost_results = None
    found_results = None
    if form.is_valid() and any(request.GET.values()):
        q = form.cleaned_data.get('search')
        cat = form.cleaned_data.get('category')
        loc = form.cleaned_data.get('location')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        lost_qs = LostItem.objects.filter(status='lost')
        found_qs = FoundItem.objects.filter(status='unclaimed')

        if q:
            lost_qs = lost_qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
            found_qs = found_qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if cat:
            lost_qs = lost_qs.filter(category=cat)
            found_qs = found_qs.filter(category=cat)
        if loc:
            lost_qs = lost_qs.filter(location__icontains=loc)
            found_qs = found_qs.filter(location__icontains=loc)
        if date_from:
            lost_qs = lost_qs.filter(date_lost__gte=date_from)
            found_qs = found_qs.filter(date_found__gte=date_from)
        if date_to:
            lost_qs = lost_qs.filter(date_lost__lte=date_to)
            found_qs = found_qs.filter(date_found__lte=date_to)

        lost_results = lost_qs.order_by('-created_at')
        found_results = found_qs.order_by('-created_at')

    return render(request, 'search_results.html', {
        'search_form': form,
        'lost_results': lost_results,
        'found_results': found_results
    })

def found(request):
    items = FoundItem.objects.filter(status="unclaimed").order_by("-created_at")
    search_query = request.GET.get("search", "").strip()

    if search_query:
        items = items.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    total_found_items = FoundItem.objects.count()
    items_returned_this_month = SuccessStory.objects.filter(
        created_at__year=date.today().year,
        created_at__month=date.today().month
    ).count()
    return_rate = round((items_returned_this_month / total_found_items) * 100) if total_found_items > 0 else 0

    context = {
        "found_items": items,
        "total_found_items": total_found_items,
        "items_returned_this_month": items_returned_this_month,
        "return_rate": f"{return_rate}%",
        "search_query": search_query,
    }

    return render(request, "found_items.html", context)

def howItWorks(request):
    return render(request, "how_it_works.html")

def successStories(request):
    """Main success stories view"""
    # Check if the model has is_published field
    model_fields = [f.name for f in SuccessStory._meta.get_fields()]
    
    if 'is_published' in model_fields:
        stories_list = SuccessStory.objects.filter(is_published=True).order_by("-created_at")
    else:
        stories_list = SuccessStory.objects.all().order_by("-created_at")
    
    # Pagination - 9 stories per page
    paginator = Paginator(stories_list, 9)
    page_number = request.GET.get('page')
    stories = paginator.get_page(page_number)
    
    # Get featured story
    if 'is_featured' in model_fields:
        featured_story = stories_list.filter(is_featured=True).first()
    else:
        featured_story = stories_list.first()
    
    # Calculate statistics
    total_reunions = stories_list.count()
    
    # Calculate success rate
    total_lost_claimed = LostItem.objects.filter(status='claimed').count()
    total_lost = LostItem.objects.count()
    lost_success_rate = round((total_lost_claimed / total_lost * 100), 2) if total_lost > 0 else 0
    
    total_found_claimed = FoundItem.objects.filter(status='claimed').count()
    total_found = FoundItem.objects.count()
    found_success_rate = round((total_found_claimed / total_found * 100), 2) if total_found > 0 else 0
    
    overall_success_rate = round((lost_success_rate + found_success_rate) / 2) if (lost_success_rate + found_success_rate) > 0 else 94
    
    context = {
        'stories': stories,
        'featured_story': featured_story,
        'total_reunions': total_reunions,
        'total_stories': total_reunions,
        'success_rate': overall_success_rate,
        'form': SuccessStoryForm(),
    }
    
    return render(request, "success_stories.html", context)

def report_lost(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            messages.success(request, 'Lost item reported successfully.')
            return redirect('lost_detail', pk=instance.pk)
    else:
        form = LostItemForm()
    return render(request, 'report_lost.html', {'form': form})

def report_found(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            messages.success(request, 'Found item reported successfully.')
            return redirect('found_detail', pk=instance.pk)
    else:
        form = FoundItemForm()
    return render(request, 'report_found.html', {'form': form})


def found_item_detail(request, pk):
    item = get_object_or_404(FoundItem, pk=pk)
    return render(request, 'found_item_detail.html', {'item': item})

def mark_lost_claim(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    if request.method == 'POST':
        item.status = 'claimed'
        item.save()
        
        # Create success story with proper data
        title = f"Reunited: {item.title}"
        proof = request.POST.get('proof', '') if request.method == 'POST' else ''
        content = f"The lost item '{item.title}' was successfully returned to its owner. Location: {item.location}."
        
        if proof:
            content += f"\nVerification: {proof}"
        
        item_url = request.build_absolute_uri(reverse('lost_detail', args=[item.pk]))
        image_url = item.thumbnail.url if hasattr(item, 'thumbnail') and item.thumbnail else (item.image.url if item.image else '')
        
        SuccessStory.objects.create(
            title=title,
            author_name=item.reporter_name or 'Anonymous',
            content=content,
            category=item.category,
            item_url=item_url,
            image_url=image_url,
            is_published=True  # Auto-publish claim success stories
        )
        
        # Send notification emails
        try:
            subject = f"Your lost item '{item.title}' has been claimed!"
            context = {
                'reporter_name': item.reporter_name or '',
                'item_title': item.title,
                'item_url': item_url,
                'proof': proof,
            }
            html_message = render_to_string('emails/claimed_lost.html', context)
            recipient = [item.reporter_email] if item.reporter_email else []
            if recipient:
                send_mail(
                    subject,
                    render_to_string('emails/claimed_lost.txt', context),
                    settings.DEFAULT_FROM_EMAIL,
                    recipient,
                    html_message=html_message,
                    fail_silently=True
                )
        except Exception as e:
            print(f"Email error: {e}")
            pass
            
        messages.success(request, 'Lost item marked as claimed and success story created!')
    return redirect('lost_detail', pk=pk)

def mark_found_claim(request, pk):
    item = get_object_or_404(FoundItem, pk=pk)
    if request.method == 'POST':
        item.status = 'claimed'
        item.save()
        
        # Create success story
        title = f"Found item claimed: {item.title}"
        proof = request.POST.get('proof', '') if request.method == 'POST' else ''
        content = f"The found item '{item.title}' was successfully returned to its owner. Location: {item.location}."
        
        if proof:
            content += f"\nVerification: {proof}"
        
        item_url = request.build_absolute_uri(reverse('found_detail', args=[item.pk]))
        image_url = item.thumbnail.url if hasattr(item, 'thumbnail') and item.thumbnail else (item.image.url if item.image else '')
        
        SuccessStory.objects.create(
            title=title,
            author_name=item.finder_name or 'Anonymous',
            content=content,
            category=item.category,
            item_url=item_url,
            image_url=image_url,
            is_published=True  # Auto-publish claim success stories
        )
        
        # Send notification emails
        try:
            subject = f"Your found item '{item.title}' has been claimed!"
            context = {
                'finder_name': item.finder_name or '',
                'item_title': item.title,
                'item_url': item_url,
                'proof': proof,
            }
            html_message = render_to_string('emails/claimed_found.html', context)
            recipient = [item.finder_email] if item.finder_email else []
            if recipient:
                send_mail(
                    subject,
                    render_to_string('emails/claimed_found.txt', context),
                    settings.DEFAULT_FROM_EMAIL,
                    recipient,
                    html_message=html_message,
                    fail_silently=True
                )
        except Exception as e:
            print(f"Email error: {e}")
            pass
            
        messages.success(request, 'Found item marked as claimed and success story created!')
    return redirect('found_detail', pk=pk)

def get_story_detail(request, story_id):
    """API endpoint to get story details for modal"""
    from django.http import JsonResponse
    
    try:
        story = SuccessStory.objects.get(id=story_id, is_published=True)

        return JsonResponse({
            "id": story.id,
            "title": story.title,
            "author_name": story.author_name,
            "created_at": story.created_at.strftime("%B %d, %Y"),
            "category": story.get_category_display() if hasattr(story, "get_category_display") else story.category,
            "content": story.content,
            "image": story.image.url if story.image else None
        })

    except SuccessStory.DoesNotExist:
        return JsonResponse({"error": "Story not found"}, status=404)
