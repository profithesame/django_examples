from typing import Any

from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import QuerySet

from .models import Course


class OwnerMixin:
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form.valid(form)

class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/image/course/list.html'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    ...

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    ...

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
