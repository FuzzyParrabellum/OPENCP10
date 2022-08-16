from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from Troubleshootapp.models import Users, Projects, Contributors, Comments, Issues

class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print("HAS_PERMISSION de isnotauthenticated est bien appelé")
        return bool(not request.user.is_authenticated)

class IsCollaborator(BasePermission):
    
    def has_permission(self, request, view):
        print("HAS_PERMISSION EST BIEN APPELE")
        if view.__str__() == "CommentViewset":
            print("has_permission est bien appellé")
            authenticated_user = request.user.user_id
            project_id = request.parser_context['kwargs']['projects_pk']
            collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
                filter(user_id=authenticated_user)
            project_author = Projects.objects.filter(project_id=project_id,
            author_user_key=request.user)
            return collaborator_occurence.exists() or project_author.exists()
        # quand comment est appelé
        elif view.__str__() == "IssueViewset":
            print("has_permission est bien appellé")
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
        print("HAS OBJECT PERMISSION EST BIEN APPELE")
        # quand project est appelé
        if view.__str__() == "ProjectViewset":
            print("has_object_permission est bien appellé")
            authenticated_user = request.user.user_id
            project_id = obj.project_id
            
            # perm = get_object_or_404(Contributors, user_id=authenticated_user, \
            #                                         project_id=project_id)
            collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
                filter(user_id=authenticated_user)
            project_author = Projects.objects.filter(project_id=project_id,
            author_user_key=request.user)
            return collaborator_occurence.exists() or project_author.exists()
        # quand issue est appelé
        elif view.__str__() == "CommentViewset":
            print("has_object_permission est bien appellé")
            authenticated_user = request.user.user_id
            project_id = request.parser_context['kwargs']['projects_pk']
            collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
                filter(user_id=authenticated_user)
            project_author = Projects.objects.filter(project_id=project_id,
            author_user_key=request.user)
            return collaborator_occurence.exists() or project_author.exists()
        # quand comment est appelé
        elif view.__str__() == "IssueViewset":
            print("has_object_permission est bien appellé")
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
            # print(f'LA VIEW A POUR VALEUR {view.__str__()}')
            current_project = Projects.objects.get(project_id=project_id)
            author_id = current_project.author_user_key
            # print(f"user_id est de {user_id}")
            # print(f"author_id est de {author_id}")
            # print(f"authenticated_user est de {authenticated_user}")
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
    
"""
Le but de la premiere permission IsAuthor serait de check si la personne connectée
qui fait la requête d'un projet, commentaire etc en particulier en est l'auteur ou
non
"""

"""
Le but de la seconde permission qui pourrait être mélangée avec la premiere (dans ce
cas pourrait juste appeler la permission IsStaff peut-être) serait de vérifier si
un utilisateur fait partie des collaborateurs 
"""