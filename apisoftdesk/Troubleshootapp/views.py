from django.shortcuts import render, get_object_or_404
from Troubleshootapp.permissions import IsNotAuthenticated, IsAuthor
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated


from Troubleshootapp.models import Contributors, Issues, Comments, Projects, Users
from Troubleshootapp.serializers import ContributorSerializer, IssueSerializer, \
    CommentSerializer, ProjectListSerializer, ProjectDetailSerializer, SignUpSerializer
# Create your views here.


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

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

class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    permissions_classes = [IsAuthenticated, IsAuthor]

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    

    def get_queryset(self):
        return Projects.objects.all()

class SignUpViewset(GenericViewSet):

    queryset = Users.objects.all()

    serializer_class = SignUpSerializer

    permissions_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)