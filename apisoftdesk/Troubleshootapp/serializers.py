from rest_framework.serializers import ModelSerializer, RelatedField, PrimaryKeyRelatedField
from django.contrib.auth.hashers import make_password


from Troubleshootapp.models import Contributors, Issues, Comments, Projects, Users


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ["user_id", "project_id", "role", "permission"]


class ContributorDetailSerializer(ModelSerializer):

        class Meta:
            model = Contributors
            fields = ["user_id", "project_id", "role", "permission"]

class IssueSerializer(ModelSerializer):

    class Meta:
            model = Issues
            fields = ["author_user_key", "title", "desc", "tag", "priority", "status", "assignee_user_key"]
            optional_fields = ["assignee_user_key"]
            read_only_fields = ["author_user_key"]

    def create(self, validated_data, **kwargs):
        projects_pk = self.context["projects_pk"]
        user_id = self.context['request'].user
        
        return Issues.objects.create(author_user_key=user_id, project_id=projects_pk, \
            **validated_data)


class CommentSerializer(ModelSerializer):
    
    class Meta:
            model = Comments
            fields = ["comment_id", "description", "author_user_id", \
                "issue_id", "created_time"]
            read_only_fields = ["comment_id",'author_user_id', "issue_id", \
                "created_time"]

    def create(self, validated_data, **kwargs):
        issues_pk = Issues.objects.get(id=self.context["issues_pk"])
        user_id = self.context['request'].user
        
        return Comments.objects.create(author_user_id=user_id, \
            issue_id=issues_pk ,**validated_data)

class ProjectListSerializer(ModelSerializer):
    
    class Meta:
        model = Projects
        fields = ["project_id", "title", "description", "type", "author_user_key"]
        read_only_fields = ["project_id", "author_user_key"]

    def create(self, validated_data):
        user_id = self.context['request'].user
        return Projects.objects.create(author_user_key=user_id, **validated_data)



class ProjectDetailSerializer(ModelSerializer):
    
    class Meta:
        model = Projects
        fields = ["project_id", "title", "description", "type", "author_user_key"]
        read_only_fields = ["project_id", "author_user_key"]

class SignUpSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ["first_name", "last_name", "email", "password"]

    def validate_password(self, value):
        return make_password(value)


