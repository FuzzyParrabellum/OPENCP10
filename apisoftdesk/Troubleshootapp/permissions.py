from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from Troubleshootapp.models import Users, Projects, Contributors

class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print("HAS_PERMISSION de isnotauthenticated est bien appelé")
        return bool(not request.user.is_authenticated)

class IsCollaborator(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        print("has_object_permissione st bien appellé")
        authenticated_user = request.user.user_id
        # user_id = obj.user_id
        # project_id = obj.project_id
        project_id = obj
        """on pourrait plutot juste regarder le request.user et le project_id, pour
        voir le project_id on pourrait juste selectionner la 1ere entrée du queryset
        et voir quel est son project_id avant de l'envoyer pour check la permission
        ça permettrait d'utiliser cette permission pour les coments aussi je pense"""
        print("perm va être appellé")
        # perm = get_object_or_404(Contributors, user_id=authenticated_user, \
        #                                         project_id=project_id)
        collaborator_occurence = Contributors.objects.filter(project_id=project_id).\
            filter(user_id=authenticated_user)

        return collaborator_occurence.exists()
    # deuxième check qui vérifie si est un auteur, donne alors plus de droits
    pass    

class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        authenticated_user = request.user
        user_id = obj.author_user_key
        project_id = obj.project_id

        current_project = Projects.objects.get(project_id=project_id)
        author_id = current_project.author_user_key

        print(f"user_id est de {user_id}")
        print(f"author_id est de {author_id}")
        print(f"authenticated_user est de {authenticated_user}")
        return authenticated_user == author_id
    
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