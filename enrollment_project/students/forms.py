# students/forms.py
from django import forms
from .models import Student, Course

class StudentForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # multiple checkboxes
        required=False
    )

    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'courses']