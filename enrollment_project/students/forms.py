# students/forms.py
from django import forms
from .models import Student, Course, Enrollment

# 1. Student Form (with Multiple Course Selection)
class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'courses']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

# 2. Course Form
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter course details...', 'rows': 3}),
        }

# 3. Enrollment Form (With Fixed Dropdown and Duplicate Prevention)
class EnrollmentForm(forms.ModelForm):
    # This explicitly creates the dropdown for Status
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Enrolled', 'Enrolled'),
        ('Completed', 'Completed'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """
        Custom Back-end Validation:
        1. Prevents duplicate enrollments for new records[cite: 13, 37, 40].
        2. Allows status updates for existing records without triggering duplicate errors.
        """
        cleaned_data = super().clean()
        student = cleaned_data.get("student")
        course = cleaned_data.get("course")

        # Duplicate Prevention Logic 
        # self.instance.pk is None only when we are CREATING a new enrollment [cite: 21, 27]
        if self.instance.pk is None: 
            if Enrollment.objects.filter(student=student, course=course).exists():
                raise forms.ValidationError(
                    f"Action Denied: {student.name} is already enrolled in {course.name}!"
                )
        
        return cleaned_data