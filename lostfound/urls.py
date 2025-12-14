from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('found/', views.found, name='found'),
    path('report/lost/', views.report_lost, name='report_lost'),
    path('report/found/', views.report_found, name='report_found'),
    path('found/<int:pk>/', views.found_item_detail, name='found_detail'),
    path('lost/<int:pk>/claim/', views.mark_lost_claim, name='mark_lost_claim'),
    path('found/<int:pk>/claim/', views.mark_found_claim, name='mark_found_claim'),
    path('search/', views.search_results, name='search_results'),
    path('how_it_works/', views.howItWorks, name='howItWorks'),
    path('success_stories/', views.successStories, name='successStories'),
    path('submit_success_story/', views.submit_success_story, name='submit_success_story'),
    path("stories/<int:story_id>/", views.get_story_detail, name="get_story_detail"),

]