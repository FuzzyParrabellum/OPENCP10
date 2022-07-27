from rest_framework.permissions import BasePermission

from Troubleshootapp.models import Users, Projects, Contributors

class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print("HAS_PERMISSION de isnotauthenticated est bien appelé")
        return bool(not request.user.is_authenticated)

class IsCollaborator(BasePermission):
    # premier check qui vérifie si est dans une liste de collaborateurs ou
    # est un auteur, donne alors des droits de read etc.
    # Pour ça il faudrait déjà que je puisse rajouter un collaborateur pour
    # faire des tests
    # ça suppose au moins trois users, un auteur, un collaborateur et juste un
    # connecté pour voir ensuite leur niveau de permission
    def has_object_permission(self, request, view, obj):
        authenticated_user = request.user
        user_id = obj.user_id
        project_id = obj.project_id

        

    # deuxième check qui vérifie si est un auteur, donne alors plus de droits
    pass    

class IsAuthor(BasePermission):
    print("------------ISAUTHOR EST BIEN APPELLE-------------")

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