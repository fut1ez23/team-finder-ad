import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from users.forms import (
    CustomPasswordChangeForm,
    LoginForm,
    ProfileEditForm,
    RegistrationForm,
)
from users.models import Skill, User

PAGE_SIZE = 12


def _build_query_prefix(request, exclude=("page",)):
    params = request.GET.copy()
    for key in exclude:
        params.pop(key, None)
    encoded = params.urlencode()
    return f"{encoded}&" if encoded else ""


def register(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("projects:list")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


@require_GET
def logout_view(request):
    logout(request)
    return redirect("projects:list")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:detail", user_id=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:detail", user_id=request.user.pk)
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {"form": form})


@require_GET
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, "users/user-details.html", {"user": user})


@require_GET
def participants_list(request):
    participants = User.objects.all().order_by("-id")
    active_skill = request.GET.get("skill", "")
    all_skills = list(
        Skill.objects.order_by("name").values_list("name", flat=True).distinct()
    )

    if active_skill:
        participants = participants.filter(skills__name=active_skill).distinct()

    paginator = Paginator(participants, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "users/participants.html",
        {
            "participants": participants,
            "page_obj": page_obj,
            "all_skills": all_skills,
            "active_skill": active_skill,
            "query_prefix": _build_query_prefix(request),
        },
    )


@require_GET
def skills_autocomplete(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[:10]
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def add_skill(request, user_id):
    if request.user.pk != user_id:
        return JsonResponse({"error": "forbidden"}, status=403)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        body = request.POST

    user = request.user
    skill_id = body.get("skill_id")
    name = (body.get("name") or "").strip()
    created = False
    added = False

    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse({"error": "bad request"}, status=400)

    if not user.skills.filter(pk=skill.pk).exists():
        user.skills.add(skill)
        added = True

    return JsonResponse(
        {
            "skill_id": skill.id,
            "id": skill.id,
            "name": skill.name,
            "created": created,
            "added": added,
        }
    )


@login_required
@require_POST
def remove_skill(request, user_id, skill_id):
    if request.user.pk != user_id:
        return JsonResponse({"error": "forbidden"}, status=403)

    user = request.user
    skill = get_object_or_404(Skill, pk=skill_id)
    if user.skills.filter(pk=skill.pk).exists():
        user.skills.remove(skill)
    return JsonResponse({"status": "ok"})
