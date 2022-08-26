from django.shortcuts import render, get_object_or_404

# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from Troubleshootapp.permissions import IsCollaborator, IsNotAuthenticated, \
    IsAuthor
from Troubleshootapp.models import Contributors, Issues, Comments, Projects, Users
from Troubleshootapp.serializers import ContributorSerializer, IssueSerializer, \
    CommentSerializer, ProjectListSerializer, ProjectDetailSerializer, SignUpSerializer, \
    ContributorDetailSerializer
# Create your views here.


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        if self.action == 'destroy' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class ContributorViewset(ModelViewSet, MultipleSerializerMixin):

    permission_classes = [IsAuthenticated, IsCollaborator]

    serializer_class = ContributorSerializer
    detail_serializer_class = ContributorDetailSerializer

    def list(self, request, projects_pk=None):
        queryset = Contributors.objects.filter(project_id=projects_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, projects_pk=None):
        queryset = Contributors.objects.filter(project_id=projects_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, users_pk=None, projects_pk=None):
        contributor_to_remove = get_object_or_404(Contributors, user_id=users_pk, \
            project_id=projects_pk)
        contributor_to_remove.delete()
        return Response({"Success":"Le collaborateur a bien été supprimé du projet."}, \
            status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, users_pk=None, projects_pk=None):
        queryset = get_object_or_404(Contributors, user_id=users_pk, \
            project_id=projects_pk)
        serializer = ContributorSerializer(queryset)
        return Response(serializer.data)

    def get_queryset(self):
        return Contributors.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj



class IssueViewset(ModelViewSet):

    def get_permissions(self):
        if self.action in ['destroy', 'update']:
            self.permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ['create', 'retrieve', 'list']:
            self.permission_classes = [IsAuthenticated, IsCollaborator]
        else:
            self.permission_classes = [IsAdminUser]
        return super(IssueViewset, self).get_permissions()

    serializer_class = IssueSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["projects_pk"] = self.request.parser_context['kwargs']['projects_pk']
        return context

    def destroy(self, request, pk=None, projects_pk=None):
        issue_to_remove = get_object_or_404(Issues, id=pk, \
            project_id=projects_pk)
        self.check_object_permissions(self.request, issue_to_remove)
        issue_to_remove.delete()
        return Response({"Success":"Le problème a bien été supprimé du projet."}, \
            status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Issues.objects.all()

    def __str__(self):
        return "IssueViewset"

class CommentViewset(ModelViewSet):

    def get_permissions(self):
        if self.action in ['destroy', 'update']:
            self.permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ['create', 'retrieve', 'list']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super(CommentViewset, self).get_permissions()

    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["issues_pk"] = self.request.parser_context['kwargs']['issues_pk']
        return context

    def destroy(self, request, projects_pk=None, pk=None, issues_pk=None):
        comment_to_remove = get_object_or_404(Comments, comment_id=pk, \
            issue_id=issues_pk)
        self.check_object_permissions(self.request, comment_to_remove)
        comment_to_remove.delete()
        return Response({"Success":"Le commentaire a bien été supprimé du problème."}, \
            status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Comments.objects.all()

    def __str__(self):
        return "CommentViewset"

class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    def get_permissions(self):
        if self.action in ['destroy', 'update']:
            self.permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ['create', 'list']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve']:
            self.permission_classes = [IsAuthenticated, IsCollaborator]
        else:
            self.permission_classes = [IsAdminUser]
        return super(ProjectViewset, self).get_permissions()

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
       return Projects.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def __str__(self):
        return "ProjectViewset"

    
class SignUpViewset(ModelViewSet):

    
    permission_classes = [AllowAny,]
    authentication_classes = []

    queryset = Users.objects.all()

    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)