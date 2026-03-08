# downloader/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("",           views.home,           name="home"),
    path("start/",     views.start_download, name="start"),
    path("tasks/",     views.all_tasks,      name="tasks"),
    path("cancel/<str:task_id>/", views.cancel, name="cancel"),
    path("pause/<str:task_id>/",  views.pause,  name="pause"),

    # ← New: streams the file to the user's browser
    path("serve/<str:task_id>/",  views.serve_file, name="serve"),


]