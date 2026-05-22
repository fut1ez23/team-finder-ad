import json
from http import HTTPStatus

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from projects.service import build_query_prefix, paginate
from users.forms import (
    LoginForm,
    PasswordChangeForm,
    ProfileEditForm,
    RegistrationForm,
)
from users.models import Skill, User

SKILLS_AUTOCOMPLETE_LIMIT = 10


def register(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("users:login")
    return render(request, "users/register.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.user)
        return redirect("projects:list")
    return render(request, "users/login.html", {"form": form})


@require_GET
def logout_view(request):
    logout(request)
    return redirect("projects:list")


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect("users:detail", user_id=request.user.pk)
    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("users:detail", user_id=request.user.pk)
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

    page_obj = paginate(participants, request.GET.get("page"))

    return render(
        request,
        "users/participants.html",
        {
            "participants": participants,
            "page_obj": page_obj,
            "all_skills": all_skills,
            "active_skill": active_skill,
            "query_prefix": build_query_prefix(request),
        },
    )


@require_GET
def skills_autocomplete(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[
        :SKILLS_AUTOCOMPLETE_LIMIT
    ]
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def add_skill(request, user_id):
    if request.user.pk != user_id:
        return JsonResponse({"error": "forbidden"}, status=HTTPStatus.FORBIDDEN)

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
        return JsonResponse({"error": "bad request"}, status=HTTPStatus.BAD_REQUEST)

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
        return JsonResponse({"error": "forbidden"}, status=HTTPStatus.FORBIDDEN)

    user = request.user
    skill = get_object_or_404(Skill, pk=skill_id)
    if user.skills.filter(pk=skill.pk).exists():
        user.skills.remove(skill)
    return JsonResponse({"status": "ok"})
