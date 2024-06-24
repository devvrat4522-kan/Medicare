from django.urls import path, include
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("prediction/",views.predictions,name="prediction"),
    path("aboutus/",views.aboutus,name="about-us"),
    path("contactus/",views.contactus,name="contact-us"),
    path("history/",views.history,name="contact-us"),
    path("generate_pdf/<int:symptom_id>/",views.generate_pdf,name="generate_pdf"),
]
