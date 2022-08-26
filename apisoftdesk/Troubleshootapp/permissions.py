from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from Troubleshootapp.models import Users, Projects, Contributors, Comments, Issues

class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user.is_authenticated)

class IsCollaborator(BasePermission):
    
    def has_permission(self, request, view):
        if view.__str__() == "CommentViewset":
            authenticated_user = request.user.user_id
            project_id = request.parser_context['kwargs']['projects_pk']
            collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
                filter(user_id=authenticated_user)
            project_author = Projects.objects.filter(project_id=project_id,
            author_user_key=request.user)
            return collaborator_occurence.exists() or project_author.exists()

        elif view.__str__() == "IssueViewset":
            authenticated_user = request.user.user_id
            project_id = request.parser_context['kwargs']['projects_pk']
            collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
                filter(user_id=authenticated_user)
            project_author = Projects.objects.filter(project_id=project_id,
            author_user_key=request.user)
            return collaborator_occurence.exists() or project_author.exists()

        else:
            return False  

    def has_object_permission(self, request, view, obj):
        # quand project est appelé
        if view.__str__() == "ProjectViewset":
            authenticated_user = request.user.user_id
            project_id = obj.project_id
            collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
                filter(user_id=authenticated_user)
            project_author = Projects.objects.filter(project_id=project_id,
            author_user_key=request.user)
            return collaborator_occurence.exists() or project_author.exists()

        # quand comment est appelé
        elif view.__str__() == "CommentViewset":
            authenticated_user = request.user.user_id
            project_id = request.parser_context['kwargs']['projects_pk']
            collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
                filter(user_id=authenticated_user)
            project_author = Projects.objects.filter(project_id=project_id,
            author_user_key=request.user)
            return collaborator_occurence.exists() or project_author.exists()

        # quand issue est appelé
        elif view.__str__() == "IssueViewset":
            authenticated_user = request.user.user_id
            project_id = request.parser_context['kwargs']['projects_pk']
            collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
                filter(user_id=authenticated_user)
            project_author = Projects.objects.filter(project_id=project_id,
            author_user_key=request.user)
            return collaborator_occurence.exists() or project_author.exists()

        else:
            return False  

class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.__str__() == "ProjectViewset":
            authenticated_user = request.user
            user_id = obj.author_user_key
            project_id = obj.project_id
            current_project = Projects.objects.get(project_id=project_id)
            author_id = current_project.author_user_key
            return authenticated_user == author_id
        elif view.__str__() == "CommentViewset":
            authenticated_user = request.user
            user_id = obj.author_user_id
            comment_id = obj.comment_id
            current_comment = Comments.objects.get(comment_id=comment_id)
            author_id = current_comment.author_user_id
            return authenticated_user == author_id
        elif view.__str__() == "IssueViewset":
            authenticated_user = request.user
            user_id = obj.author_user_key
            issue_id = obj.id
            current_issue = Issues.objects.get(id=issue_id)
            author_id = current_issue.author_user_key
            return authenticated_user == author_id
        else:
            return False
    