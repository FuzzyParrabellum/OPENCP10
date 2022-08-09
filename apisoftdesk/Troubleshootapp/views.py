from django.shortcuts import render, get_object_or_404
from Troubleshootapp.permissions import IsCollaborator, IsNotAuthenticated, IsAuthor
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


from Troubleshootapp.models import Contributors, Issues, Comments, Projects, Users
from Troubleshootapp.serializers import ContributorSerializer, IssueSerializer, \
    CommentSerializer, ProjectListSerializer, ProjectDetailSerializer, SignUpSerializer, \
    ContributorDetailSerializer
# Create your views here.


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        print("------get-serializer-class est bien appellée----")
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        if self.action == 'destroy' and self.detail_serializer_class is not None:
            print("-------L'action delete est bien appellée--------")
            return self.detail_serializer_class
        return super().get_serializer_class()

class ContributorViewset(ModelViewSet, MultipleSerializerMixin):

    # est pour l'instant bloqué car il y aurait besoin d'un queryset de base (je pense)
    # et non pas d'un queryset pour chaque méthode pour que get_object soit appelé
    # et donc que la permission que l'on souhaite, isCollaborator soit appellée
    permission_classes = [IsAuthenticated, IsCollaborator]

    serializer_class = ContributorSerializer
    detail_serializer_class = ContributorDetailSerializer

    def list(self, request, projects_pk=None):
        print("ACTION LISTE BIEN APPELLEE")
        queryset = Contributors.objects.filter(project_id=projects_pk)
        # queryset = self.get_queryset().objects.filter(project_id=projects_pk)
        # self.check_object_permissions(self.request, projects_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, projects_pk=None):
        queryset = Contributors.objects.filter(project_id=projects_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, users_pk=None, projects_pk=None):
        print("l'action de delete est bien appellée dans contributorVIEWSET")
        contributor_to_remove = get_object_or_404(Contributors, user_id=users_pk, \
            project_id=projects_pk)
        contributor_to_remove.delete()
        return Response({"Success":"Le collaborateur a bien été supprimé du projet."}, \
            status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, users_pk=None, projects_pk=None):
        print("l'action de retrieve est bien appellée dans contributorVIEWSET")
        queryset = get_object_or_404(Contributors, user_id=users_pk, \
            project_id=projects_pk)
        # queryset = Contributors.objects.filter(user_id=pk, project_id=projects_pk)
        serializer = ContributorSerializer(queryset)
        return Response(serializer.data)

    def get_queryset(self):
        print("get_queryset est bien appellée")
        return Contributors.objects.all()

    def get_object(self):
        ("le get_object de contributor est bien appelé")
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj



class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    # def create(self, request, projects_pk=None):
    #     print("la methode create est bien appellée")
    #     queryset = Issues.objects.filter(project_id=projects_pk)
    #     # context = {"projects_pk": projects_pk}
    #     # serializer = IssueSerializer(queryset, many=True, context=context)
    #     serializer = IssueSerializer(queryset, many=True)
    #     # serializer.save(author_user_key=request.user.user_id, project_id=projects_pk)
    #     return Response(serializer.data)

    def get_queryset(self):
        return Issues.objects.all()

class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()

class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
#class ProjectViewset(ModelViewSet):
    
    # queryset = Projects.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
       return Projects.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    

    

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