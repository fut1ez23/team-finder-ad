from django import forms

from projects.models import Project
from users.validators import validate_github_url


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[("open", "Открыт"), ("closed", "Закрыт")],
        label="Статус",
    )

    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")
        labels = {
            "name": "Название",
            "description": "Описание",
            "github_url": "Ссылка на GitHub",
        }

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url", ""))
