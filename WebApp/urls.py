from django.urls import path
from . import views

urlpatterns = [
    path("upload", views.upload, name="upload"),
    path("login", views.login, name="login"),
    path("sign-up", views.signup, name="signup"),
    path("", views.homepage, name="homepage"),
    path("logout", views.logout, name="logout"),
    path("askquestion", views.askquestion, name="askquestion"),
    path("choosefile", views.choosefile, name="choosefile"),
    path("delete", views.delete, name="delete"),
    path("help", views.help, name="help"),
    path("terms", views.terms, name="terms"),
    path("get_text", views.get_text, name="get_text"),
    path("get_page_info", views.get_page_info, name="get_page_info"),
    path("get_paragraph_info", views.get_paragraph_info, name="get_paragraph_info"),
]