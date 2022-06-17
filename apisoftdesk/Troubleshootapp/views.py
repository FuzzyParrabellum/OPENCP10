from django.shortcuts import render
from Troubleshootapp.permissions import IsNotAuthenticated
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet


from Troubleshootapp.models import Contributors, Issues, Comments, Projects, Users
from Troubleshootapp.serializers import ContributorSerializer, IssueSerializer, \
    CommentSerializer, ProjectSerializer, SignUpSerializer
# Create your views here.

class ContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributors.objects.all()

class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issues.objects.all()

class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()

class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    # detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Projects.objects.all()

class SignUpViewset(GenericViewSet):

    queryset = Users.objects.all()

    serializer_class = SignUpSerializer

    permissions_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)