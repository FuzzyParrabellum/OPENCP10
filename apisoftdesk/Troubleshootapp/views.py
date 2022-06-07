from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from Troubleshootapp.models import Contributors, Issues, Comments, Projects
from Troubleshootapp.serializers import ContributorSerializer, IssueSerializer, CommentSerializer, ProjectSerializer
# Create your views here.

class ContributorViewset():

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributors.objects.all()

class IssueViewset():

    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issues.objects.all()

class CommentViewset():

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()

class ProjectViewset():

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.all()