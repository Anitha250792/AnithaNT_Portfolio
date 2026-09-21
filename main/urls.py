from django.urls import path

from . import views

# URL names are unchanged from the original multi-page site, so existing
# {% url %} tags, links and emails keep working.
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),          # -> /#about
    path("projects/", views.projects, name="projects"),  # -> /#projects
    path("contact/", views.contact, name="contact"),     # form endpoint
]
