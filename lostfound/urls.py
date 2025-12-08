from django.urls import path
from . import views

urlpatterns =[
    path ('',views.home,name='home'),
    path('lostItems/',views.lostItems, name = 'lostItems'),
    path("found/", views.found, name="found"),
    path("how_it_works/", views.howItWorks, name = "howItWorks"),
    path("success_stories/", views.successStories, name = "successStories"),
]

