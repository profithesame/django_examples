from django.shortcuts import get_object_or_404
from django.http import HttpRequest

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from courses.models import Subject, Course
from courses.api.permissions import IsEnrolled
from courses.api.serializers import (SubjectSerializer, 
    CourseSerializer,
    CourseWithContentsSerializer,
)

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated])
    def enroll(self, request: HttpRequest, *args, **kwargs) -> Response:
        course = self.get_object()
        course.students.add(request.user)

        return Response(
            {
                'enrolled': True,
            }
        )

    @action(detail=True,
            methods=['get'],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request: HttpRequest, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
