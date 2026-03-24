from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("", views.home_redirect, name="home_redirect"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("redirect-dashboard/", views.redirect_dashboard, name="redirect_dashboard"),

    path("dashboard/", views.redirect_dashboard, name="dashboard"),

    path("sales-dashboard/", views.sales_dashboard, name="sales_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("add-lead/", views.register, name="register"),
    path("bulk-import/", views.bulk_import_leads, name="bulk_import_leads"),
    path("edit/<int:lead_id>/", views.edit_lead, name="edit_lead"),
    path("delete/<int:lead_id>/", views.delete_lead, name="delete_lead"),
    path("api/leads/", views.api_leads, name="api_leads"),
    path("api/leads/<int:lead_id>/", views.api_lead_detail, name="api_lead_detail"),
    path("create-sales-user/", views.create_sales_user, name="create_sales_user"),
    path("contact-messages/", views.contact_messages, name="contact_messages"),
    path("login/", views.login_view, name="login"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("resend-otp/", views.resend_otp, name="resend_otp"),
]