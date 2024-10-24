from typing import Any, Dict

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.forms import BaseModelForm
from django.db.models import QuerySet
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from courses.models import Course

from .forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
            password=cd['password'])
        login(self.request, user)

        return super().form_valid(form)

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form:BaseModelForm) -> HttpResponse:
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('student_course_detail',
            args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        # get course data
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            # get first module
            context['module'] = course.modules.all()[0]

        return context
