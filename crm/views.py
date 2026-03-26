from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.db import transaction

import random
from django.core.mail import send_mail

from .models import Lead, InteractionLog, ContactMessage
from .serializers import LeadSerializer
from ml_engine.predict import predict_lead

from io import TextIOWrapper
import csv

# DRF / JWT
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")

# ================= ROLE CHECK =================

def is_admin(user):
    return user.is_staff or user.is_superuser


def is_sales(user):
    return user.is_authenticated and not (user.is_staff or user.is_superuser)


# ================= AUTH =================

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("redirect_dashboard")
    return redirect("login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("redirect_dashboard")

    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("redirect_dashboard")
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def redirect_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect("admin_dashboard")
    return redirect("sales_dashboard")


# ================= CREATE LEAD =================

@login_required
@user_passes_test(is_sales)
def register(request):
    if request.method == "POST":
        try:
            company_size = int(request.POST.get("company_size", 0))
            budget = int(request.POST.get("budget", 0))
            interaction_score = int(request.POST.get("interaction_score", 0))
        except ValueError:
            return render(request, "register.html", {"error": "Invalid input"})

        score, probability = predict_lead(company_size, budget, interaction_score)

        status_label = "Hot" if score >= 80 else "Warm" if score >= 50 else "Cold"

        lead = Lead.objects.create(
            name=request.POST.get("name", ""),
            email=request.POST.get("email", ""),
            company=request.POST.get("company", ""),
            phone=request.POST.get("phone", ""),
            source=request.POST.get("source", ""),
            industry=request.POST.get("industry", ""),
            interaction_history=request.POST.get("interaction_history", ""),
            company_size=company_size,
            budget=budget,
            interaction_score=interaction_score,
            lead_score=score,
            conversion_probability=probability,
            status=status_label,
            crm_status="New",
            assigned_to=request.user
        )

        if lead.interaction_history:
            InteractionLog.objects.create(
                lead=lead,
                note=lead.interaction_history
            )

        return render(request, "lead_result.html", {
            "score": score,
            "probability": round(probability * 100, 2),
            "status": status_label
        })

    return render(request, "register.html")


# ================= SALES DASHBOARD =================

@login_required
@user_passes_test(is_sales)
def sales_dashboard(request):
    leads = Lead.objects.filter(assigned_to=request.user).order_by("-created_at")

    high = leads.filter(status="Hot").count()
    medium = leads.filter(status="Warm").count()
    low = leads.filter(status="Cold").count()

    avg_score = leads.aggregate(avg=Avg("lead_score"))["avg"] or 0

    converted = leads.filter(crm_status="Converted").count()
    total_leads = leads.count()
    conversion_rate = (converted / total_leads * 100) if total_leads else 0

    new_leads = leads.filter(crm_status="New").count()
    contacted = leads.filter(crm_status="Contacted").count()
    qualified = leads.filter(crm_status="Qualified").count()
    lost = leads.filter(crm_status="Lost").count()

    top_leads = leads.order_by("-lead_score")[:5]

    source_data = (
        leads.values("source")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    top_converting_sources = (
        leads.filter(crm_status="Converted")
        .values("source")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    return render(request, "sales_dashboard.html", {
        "leads": leads,
        "high": high,
        "medium": medium,
        "low": low,
        "avg_score": round(avg_score, 2),
        "conversion_rate": round(conversion_rate, 2),
        "new_leads": new_leads,
        "contacted": contacted,
        "qualified": qualified,
        "converted": converted,
        "lost": lost,
        "top_leads": top_leads,
        "source_data": source_data,
        "top_converting_sources": top_converting_sources,
    })


# ================= ADMIN DASHBOARD =================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    leads = Lead.objects.all().order_by("-created_at")

    high = leads.filter(status="Hot").count()
    medium = leads.filter(status="Warm").count()
    low = leads.filter(status="Cold").count()

    top_leads = leads.order_by("-lead_score")[:5]
    warm_lead = leads.filter(status="Warm").order_by("-lead_score").first()

    avg_score = leads.aggregate(avg=Avg("lead_score"))["avg"] or 0

    source_data = (
        leads.values("source")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    new_leads = leads.filter(crm_status="New").count()
    contacted = leads.filter(crm_status="Contacted").count()
    qualified = leads.filter(crm_status="Qualified").count()
    converted = leads.filter(crm_status="Converted").count()
    lost = leads.filter(crm_status="Lost").count()

    total_leads = leads.count()
    conversion_rate = (converted / total_leads * 100) if total_leads else 0

    top_converting_sources = (
        leads.filter(crm_status="Converted")
        .values("source")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    sales_users = User.objects.filter(is_staff=False, is_superuser=False).annotate(
        total_leads=Count("assigned_leads"),
        hot_leads=Count("assigned_leads", filter=Q(assigned_leads__status="Hot")),
        warm_leads=Count("assigned_leads", filter=Q(assigned_leads__status="Warm")),
        cold_leads=Count("assigned_leads", filter=Q(assigned_leads__status="Cold")),
        converted_leads=Count("assigned_leads", filter=Q(assigned_leads__crm_status="Converted")),
        avg_user_score=Avg("assigned_leads__lead_score"),
    )

    return render(request, "dashboard.html", {
        "leads": leads,
        "high": high,
        "medium": medium,
        "low": low,
        "top_leads": top_leads,
        "warm_lead": warm_lead,
        "avg_score": round(avg_score, 2),
        "source_data": source_data,
        "new_leads": new_leads,
        "contacted": contacted,
        "qualified": qualified,
        "converted": converted,
        "lost": lost,
        "conversion_rate": round(conversion_rate, 2),
        "top_converting_sources": top_converting_sources,
        "sales_users": sales_users,
    })


# ================= EDIT LEAD =================

@login_required
@user_passes_test(is_sales)
def edit_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id, assigned_to=request.user)

    if request.method == "POST":
        lead.name = request.POST.get("name", "")
        lead.company = request.POST.get("company", "")
        lead.email = request.POST.get("email", "")
        lead.phone = request.POST.get("phone", "")
        lead.source = request.POST.get("source", "")
        lead.industry = request.POST.get("industry", "")
        lead.interaction_history = request.POST.get("interaction_history", "")
        lead.crm_status = request.POST.get("crm_status", "New")

        try:
            lead.company_size = int(request.POST.get("company_size") or 0)
            lead.budget = int(request.POST.get("budget") or 0)
            lead.interaction_score = int(request.POST.get("interaction_score") or 0)
        except ValueError:
            return render(request, "edit_lead.html", {
                "lead": lead,
                "error": "Invalid numeric input"
            })

        lead.save()

        if lead.interaction_history:
            InteractionLog.objects.create(
                lead=lead,
                note=lead.interaction_history
            )

        return redirect("sales_dashboard")

    return render(request, "edit_lead.html", {"lead": lead})


# ================= DELETE =================

@login_required
@user_passes_test(is_sales)
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id, assigned_to=request.user)
    lead.delete()
    return redirect("sales_dashboard")


# ================= BULK IMPORT =================

@login_required
@user_passes_test(is_sales)
def bulk_import_leads(request):
    message = None
    error = None

    hot = warm = cold = count = 0

    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            file_data = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(file_data)

            with transaction.atomic():
                for row in reader:
                    try:
                        company_size = int(row.get("company_size", 0))
                        budget = int(row.get("budget", 0))
                        interaction_score = int(row.get("interaction_score", 0))

                        score, prob = predict_lead(company_size, budget, interaction_score)

                        status_label = "Hot" if score >= 80 else "Warm" if score >= 50 else "Cold"

                        if status_label == "Hot":
                            hot += 1
                        elif status_label == "Warm":
                            warm += 1
                        else:
                            cold += 1

                        lead = Lead.objects.create(
                            name=row.get("name", ""),
                            email=row.get("email", ""),
                            company=row.get("company", ""),
                            phone=row.get("phone", ""),
                            source=row.get("source", ""),
                            industry=row.get("industry", ""),
                            interaction_history=row.get("interaction_history", ""),
                            company_size=company_size,
                            budget=budget,
                            interaction_score=interaction_score,
                            lead_score=score,
                            conversion_probability=prob,
                            status=status_label,
                            crm_status="New",
                            assigned_to=request.user
                        )

                        if lead.interaction_history:
                            InteractionLog.objects.create(
                                lead=lead,
                                note=lead.interaction_history
                            )

                        count += 1
                    except Exception:
                        continue

            message = f"{count} Leads Imported"

        except Exception as e:
            error = str(e)

    return render(request, "bulk_import.html", {
        "message": message,
        "error": error,
        "hot": hot,
        "warm": warm,
        "cold": cold
    })


# ================= API (JWT PROTECTED) =================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_leads(request):
    if request.method == 'GET':
        if request.user.is_staff or request.user.is_superuser:
            leads = Lead.objects.all()
        else:
            leads = Lead.objects.filter(assigned_to=request.user)

        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(assigned_to=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_lead_detail(request, lead_id):
    if request.user.is_staff or request.user.is_superuser:
        lead = get_object_or_404(Lead, id=lead_id)
    else:
        lead = get_object_or_404(Lead, id=lead_id, assigned_to=request.user)

    if request.method == 'GET':
        serializer = LeadSerializer(lead)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        lead.delete()
        return Response({"message": "Lead deleted successfully"}, status=204)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_warm_lead(request):
    if request.user.is_staff or request.user.is_superuser:
        warm_lead = Lead.objects.filter(status="Warm").order_by("-lead_score").first()
    else:
        warm_lead = Lead.objects.filter(
            status="Warm",
            assigned_to=request.user
        ).order_by("-lead_score").first()

    if warm_lead:
        serializer = LeadSerializer(warm_lead)
        return Response(serializer.data)

    return Response({"message": "No Warm Lead Found"})


# ================= EXTRA =================

@login_required
@user_passes_test(is_admin)
def create_sales_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        email = request.POST.get("email", "").strip()

        if not username or not password or not email:
            messages.error(request, "All fields are required")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")

        elif User.objects.filter(email=email).exists():   # ✅ NEW
            messages.error(request, "Email already exists")

        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user.save()

            messages.success(request, "User created successfully")
            return redirect("create_sales_user")

    return render(request, "create_sales_user.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not name or not email or not message_text:
            messages.error(request, "Please fill all fields.")
            return render(request, "contact.html")

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        messages.success(request, "Message sent successfully.")
        return redirect("contact")

    return render(request, "contact.html")

@login_required
@user_passes_test(is_admin)
def contact_messages(request):
    messages_list = ContactMessage.objects.all().order_by("-created_at")
    return render(request, "contact_messages.html", {"messages_list": messages_list})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("redirect_dashboard")

    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user:
            # Generate OTP
            otp = random.randint(100000, 999999)

            # Store in session
            request.session['otp'] = otp
            request.session['user_id'] = user.id

            # Send OTP to email
            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}',
                'your_email@gmail.com',
                [user.email],
                fail_silently=False,
            )

            return redirect("verify_otp")

        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})

def verify_otp(request):
    error = None

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        user_id = request.session.get("user_id")

        if str(entered_otp) == str(session_otp):
            user = User.objects.get(id=user_id)
            login(request, user)

            # Clear OTP after login
            request.session.pop('otp', None)

            return redirect("redirect_dashboard")
        else:
            error = "Invalid OTP"

    return render(request, "verify_otp.html", {"error": error})

from django.conf import settings

def resend_otp(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    otp = random.randint(100000, 999999)
    request.session['otp'] = otp

    send_mail(
        'Your New OTP Code',
        f'Your new OTP is {otp}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return redirect("verify_otp")