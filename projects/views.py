from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from projects.constants import CLOSED, OPEN
from projects.forms import ProjectForm
from projects.models import Project
from projects.service import build_query_prefix, paginate


@require_GET
def project_list(request):
    projects = Project.objects.select_related("owner").prefetch_related(
        "participants"
    )
    page_obj = paginate(projects, request.GET.get("page"))
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
            "page_obj": page_obj,
            "query_prefix": build_query_prefix(request),
        },
    )


@require_GET
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=project_id,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.pk or project.status != OPEN:
        return JsonResponse(
            {"error": "forbidden"}, status=HTTPStatus.FORBIDDEN
        )
    project.status = CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": CLOSED})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id == request.user.pk:
        return JsonResponse(
            {"error": "forbidden"}, status=HTTPStatus.FORBIDDEN
        )

    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        return JsonResponse({"status": "ok", "participant": False})
    project.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": True})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None, initial={"status": OPEN})
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:detail", project_id=project.pk)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.pk:
        return redirect("projects:detail", project_id=project.pk)

    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("projects:detail", project_id=project.pk)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )