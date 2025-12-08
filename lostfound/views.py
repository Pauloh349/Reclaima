from django.shortcuts import render

# Create your views here.

def lostItems(request):
    return render(request,"lost_items.html")

def home(request):
    return render(request,"home.html")

def found(request):
    return render(request, "found_items.html")

def howItWorks(request):
    return render(request, "how_it_works.html")

def successStories(request):
    return render(request, "success_stories.html")