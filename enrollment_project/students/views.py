from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .models import Student, Course, Enrollment
from .forms import StudentForm, CourseForm, EnrollmentForm
from django.db.models import Q

# --- DASHBOARD & LIST VIEWS ---

def dashboard(request):
    """Provides high-level metrics and split activity feeds."""
    total_users = Student.objects.count()
    active_courses = Course.objects.count()
    
    # Accurate count for the 'Pending' metric card
    pending_count = Enrollment.objects.filter(status='Pending').count()
    
    # Top 5 most recent records that are NOT yet completed
    recent_records = Enrollment.objects.exclude(status='Completed').order_by('-enrollment_date')[:5]
    
    # Top 5 most recent completed/closed records
    archived_records = Enrollment.objects.filter(status='Completed').order_by('-enrollment_date')[:5]

    context = {
        'total_users': total_users,
        'active_courses': active_courses,
        'pending_count': pending_count,
        'recent_records': recent_records,
        'archived_records': archived_records,
    }
    return render(request, 'students/dashboard.html', context)

def users(request):
    """Displays students with their total course enrollment count and search functionality."""
    query = request.GET.get('q')
    students = Student.objects.annotate(course_count=Count('enrollment'))

    if query:
        students = students.filter(name__icontains=query) | \
                   students.filter(email__icontains=query)
    
    return render(request, 'students/users.html', {
        'students': students, 
        'query': query
    })

def courses_list(request):
    """Displays the full catalog of courses."""
    courses = Course.objects.all()
    return render(request, 'students/courses.html', {'courses': courses})

def records_list(request):
    """Displays all active (non-completed) enrollment records with search."""
    query = request.GET.get('q') # Get the search word from the URL
    active_records = Enrollment.objects.exclude(status='Completed').select_related('student', 'course')

    if query:
        # The Q object allows us to search with "OR" logic
        active_records = active_records.filter(
            Q(student__name__icontains=query) |  # Search by Student Name
            Q(student__email__icontains=query) | # OR Student Email
            Q(course__name__icontains=query)     # OR Course Name
        )

    return render(request, 'students/records.html', {
        'records': active_records, 
        'query': query # Pass the query back so we can keep it in the search box
    })


def closed_records(request):
    """Displays the 'System Archive' of completed enrollments with search."""
    query = request.GET.get('q')
    completed_records = Enrollment.objects.filter(status='Completed').select_related('student', 'course')

    if query:
        completed_records = completed_records.filter(
            Q(student__name__icontains=query) |
            Q(student__email__icontains=query) |
            Q(course__name__icontains=query)
        )

    return render(request, 'students/closed_records.html', {
        'records': completed_records,
        'query': query
    })

# --- ADD / CREATE VIEWS ---

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New student has been added successfully!')
            return redirect('students_list')
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New course created successfully!')
            return redirect('courses_list')
    else:
        form = CourseForm()
    return render(request, 'students/add_course.html', {'form': form})

def enroll_student(request):
    """Handles new enrollments with dynamic course filtering based on existing choices."""
    student_id = request.GET.get('student')
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment successful!")
            return redirect('records_list')
    else:
        form = EnrollmentForm()

        if student_id:
            selected_student = get_object_or_404(Student, id=student_id)
            # Find courses the student has already joined
            taken_courses = Enrollment.objects.filter(student=selected_student).values_list('course_id', flat=True)
            # Filter the queryset to exclude those courses
            form.fields['course'].queryset = Course.objects.exclude(id__in=taken_courses)
            # Set the initial student in the dropdown
            form.initial['student'] = selected_student

    return render(request, 'students/enroll_student.html', {'form': form})


# --- EDIT / UPDATE VIEWS ---

def edit_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student) 
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {student.name} successfully!')
            return redirect('students_list')
    else:
        form = StudentForm(instance=student) 
    
    return render(request, 'students/add_student.html', {'form': form, 'edit_mode': True})

def edit_course(request, pk):
    course = get_object_or_404(Course, id=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.name}" updated successfully!')
            return redirect('courses_list')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'students/add_course.html', {'form': form, 'edit_mode': True})

def edit_record(request, pk):
    """
    Handles status updates for existing enrollments.
    Includes an Archive Guard to prevent modifications to 'Completed' records.
    """
    record = get_object_or_404(Enrollment, id=pk)
    
    # 1. Archive Guard
    if record.status == 'Completed':
        messages.error(request, "Action Denied: This record is archived and cannot be edited.")
        return redirect('records_list')
    
    # 2. Process Update
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Status for {record.student.name} updated successfully!")
            return redirect('records_list')
    else:
        # Pre-fill with existing record instance
        form = EnrollmentForm(instance=record)
        
    # 3. Render with 'record' object to fix 'VariableDoesNotExist' in template
    return render(request, 'students/enroll_student.html', {
        'form': form, 
        'edit_mode': True,
        'record': record 
    })


# --- DELETE VIEWS ---

def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    name = student.name
    student.delete()
    messages.warning(request, f'Student "{name}" has been removed.')
    return redirect('students_list')

def delete_course(request, pk):
    course = get_object_or_404(Course, id=pk)
    course_name = course.name
    course.delete()
    messages.warning(request, f'Course "{course_name}" has been deleted.')
    return redirect('courses_list')
