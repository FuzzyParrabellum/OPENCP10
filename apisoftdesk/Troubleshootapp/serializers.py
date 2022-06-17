from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password


from Troubleshootapp.models import Contributors, Issues, Comments, Projects, Users


class ContributorSerializer(ModelSerializer):
    pass

class IssueSerializer(ModelSerializer):
    pass

class CommentSerializer(ModelSerializer):
    pass

class ProjectSerializer(ModelSerializer):
    pass

class SignUpSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ["first_name", "last_name", "email", "password"]

    def validate_password(self, value):
        return make_password(value)


