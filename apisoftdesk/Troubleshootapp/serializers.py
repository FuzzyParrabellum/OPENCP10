from rest_framework.serializers import ModelSerializer, RelatedField, PrimaryKeyRelatedField
from django.contrib.auth.hashers import make_password


from Troubleshootapp.models import Contributors, Issues, Comments, Projects, Users


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ["user_id", "project_id", "role", "permission"]

    # peut vérifier ici au moment de créer le contributeur si il n'est pas déjà 
    # l'auteur du projet, dans ce cas ne pas autoriser de le mettre en contributeur
    # faudrait aussi peut-être vérifier que l'utilisateur n'est pas déjà contributeur
    # sur le projet

class ContributorDetailSerializer(ModelSerializer):

        class Meta:
            model = Contributors
            fields = ["user_id", "project_id", "role", "permission"]

class IssueSerializer(ModelSerializer):

    # author_user_key = PrimaryKeyRelatedField(queryset=Users.objects.all(), \
    #     many=False, read_only=False)

    class Meta:
            model = Issues
            # fields = ["title", "desc", "tag", "priority", "status", "author_user_key"]
            fields = ["title", "desc", "tag", "priority", "status"]

    # def create(self, validated_data):
    #     projects_pk = self.context.get("projects_pk")
    #     user_id = self.context['request'].user
    #     print(f'user_id est d abord égal à {user_id}')
    #     # user_id = Users.objects.get(user_id=user_id)
    #     print(f"projects_pk est bien égal à {projects_pk}")
    #     print(f'user_id est égal à {user_id}')
    #     print(f"self.context est égal à {self.context}")
    #     return Issues.objects.create(author_user_key=user_id, project_id=2, \
    #         **validated_data)


class CommentSerializer(ModelSerializer):
    pass

class ProjectListSerializer(ModelSerializer):
    
    # author_user_key = Field(source='Projects.author_user_key')
    author_user_key = RelatedField(source='Users', read_only=True)


    class Meta:
        model = Projects
        fields = ["title", "description", "type", "author_user_key"]
        # read_only_fields = ["project_id", "author_user_key"]

    def create(self, validated_data):
        user_id = self.context['request'].user
        print(f'user_id au moment de créer un projet est de {user_id}')
        return Projects.objects.create(author_user_key=user_id, **validated_data)



class ProjectDetailSerializer(ModelSerializer):
    
    class Meta:
        model = Projects
        fields = ["project_id", "title", "description", "type", "author_user_key"]

class SignUpSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ["first_name", "last_name", "email", "password"]

    def validate_password(self, value):
        return make_password(value)


