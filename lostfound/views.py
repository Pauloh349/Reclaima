from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from .models import LostItem, FoundItem, SuccessStory
from django.db.models import Q
from .forms import LostItemForm, FoundItemForm, SearchForm


def lostItems(request):
    items = LostItem.objects.filter(status="lost").order_by("-created_at")
    return render(request, "lost_items.html", {"lost_items": items})


def home(request):
    # handle optional search via GET
    form = SearchForm()
    recent_lost = LostItem.objects.all().order_by("-created_at")[:3]
    recent_found = FoundItem.objects.all().order_by("-created_at")[:3]
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
            lost_qs = lost_qs.filter(title__iexact=q)
            found_qs = found_qs.filter(title__iexact=q)
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

    stats = {
        "items_reunited": SuccessStory.objects.count() * 10,
        "success_rate": "95%",
        "avg_recovery": "24h",
    }

    return render(request, "home.html", {
        "recent_lost": recent_lost,
        "recent_found": recent_found,
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
            lost_qs = lost_qs.filter(title__iexact=q)
            found_qs = found_qs.filter(title__iexact=q)
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

    return render(request, 'search_results.html', {'search_form': form, 'lost_results': lost_results, 'found_results': found_results})


def found(request):
    from datetime import date
    from django.db.models import Count

    items = FoundItem.objects.filter(status="unclaimed").order_by("-created_at")
    
    total_found_items = items.count()
    items_returned_this_month = SuccessStory.objects.filter(
        created_at__year=date.today().year,
        created_at__month=date.today().month
    ).count()
    
    # Calculate a simple return rate (avoid division by zero)
    if total_found_items > 0:
        return_rate = (items_returned_this_month / total_found_items) * 100
        return_rate = round(return_rate) # Round to nearest whole number
    else:
        return_rate = 0
    
    context = {
        "found_items": items,
        "total_found_items": total_found_items,
        "items_returned_this_month": items_returned_this_month,
        "return_rate": f"{return_rate}%"
    }
    return render(request, "found_items.html", context)


def howItWorks(request):
    return render(request, "how_it_works.html")


def successStories(request):
    stories = SuccessStory.objects.all().order_by("-created_at")
    return render(request, "success_stories.html", {"stories": stories})


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


def lost_item_detail(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    return render(request, 'lost_item_detail.html', {'item': item})


def found_item_detail(request, pk):
    item = get_object_or_404(FoundItem, pk=pk)
    return render(request, 'found_item_detail.html', {'item': item})


def mark_lost_claim(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    if request.method == 'POST':
        item.status = 'claimed'
        item.save()
        # create success story (with optional item link and image url)
        title = f"Reunited: {item.title}"
        proof = request.POST.get('proof', '') if request.method == 'POST' else ''
        content = f"The lost item '{item.title}' reported by {item.reporter_name or 'a user'} was marked as claimed. Location: {item.location}."
        item_url = request.build_absolute_uri(reverse('lost_detail', args=[item.pk]))
        image_url = item.thumbnail.url if getattr(item, 'thumbnail', None) else (item.image.url if item.image else '')
        SuccessStory.objects.create(title=title, author_name=item.reporter_name or '', content=content + ("\nProof: " + proof if proof else ''), category=item.category, item_url=item_url, image_url=image_url)
        # send notification emails if addresses available (HTML + plain)
        try:
            subject = f"Your lost item '{item.title}' status updated"
            context = {
                'reporter_name': item.reporter_name or '',
                'item_title': item.title,
                'item_url': item_url,
                'proof': proof,
            }
            html_message = render_to_string('emails/claimed_lost.html', context)
            recipient = [item.reporter_email] if item.reporter_email else []
            if recipient:
                send_mail(subject, render_to_string('emails/claimed_lost.html', context), settings.DEFAULT_FROM_EMAIL, recipient, html_message=html_message, fail_silently=True)
        except Exception:
            pass
        messages.success(request, 'Lost item marked as claimed.')
    return redirect('lost_detail', pk=pk)

def found(request):
    items = FoundItem.objects.filter(status="unclaimed").order_by("-created_at")
    return render(request, "found_items.html", {"found_items": items})


def mark_found_claim(request, pk):
    item = get_object_or_404(FoundItem, pk=pk)
    if request.method == 'POST':
        item.status = 'claimed'
        item.save()
        title = f"Found item claimed: {item.title}"
        proof = request.POST.get('proof', '') if request.method == 'POST' else ''
        content = f"The found item '{item.title}' reported by {item.finder_name or 'a user'} was marked as claimed. Location: {item.location}."
        item_url = request.build_absolute_uri(reverse('found_detail', args=[item.pk]))
        image_url = item.thumbnail.url if getattr(item, 'thumbnail', None) else (item.image.url if item.image else '')
        SuccessStory.objects.create(title=title, author_name=item.finder_name or '', content=content + ("\nProof: " + proof if proof else ''), category=item.category, item_url=item_url, image_url=image_url)
        try:
            subject = f"Your found item '{item.title}' status updated"
            context = {'finder_name': item.finder_name or '', 'item_title': item.title, 'item_url': item_url, 'proof': proof}
            html_message = render_to_string('emails/claimed_found.html', context)
            recipient = [item.finder_email] if item.finder_email else []
            if recipient:
                send_mail(subject, render_to_string('emails/claimed_found.html', context), settings.DEFAULT_FROM_EMAIL, recipient, html_message=html_message, fail_silently=True)
        except Exception:
            pass
        messages.success(request, 'Found item marked as claimed.')
    return redirect('found_detail', pk=pk)


def signin(request):
    """Handle user sign in"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'signin.html')


def signup(request):
    """Handle user sign up"""
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'signup.html')
