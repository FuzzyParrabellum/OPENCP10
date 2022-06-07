from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from django.conf import settings
# Create your models here.

class Users(AbstractUser):
    pass

class Contributors(models.Model):

    user_id = models.IntegerField()
    project_id = models.IntegerField()
    # IIMPORTANT : apparrement choicefield se trouve plutôt sur forms, que faire de l'info?
    # permission = models.ChoiceField()
    role = models.CharField(max_length=255)

class Projects(models.Model):

    PROJECT_TYPES = [
        ('back','back-end'),
        ('front', 'front-end'),
        ('ios', 'iOS'),
        ('android', 'Android')
    ]

    project_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(choices=PROJECT_TYPES, max_length=7)
    # Doit compléter la ForeignKey en-dessous
    author_user_key = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Issues(models.Model):

    ISSUES_PRIORITIES = (
        ('low', 'FAIBLE'),
        ('medium', 'MOYENNE'),
        ('high', 'ÉLEVÉE')
    )
    ISSUES_TAGS = (
        ('bug', 'BUG'),
        ('better', 'AMÉLIORATION'),
        ('task', 'TÂCHE')
    )
    ISSUES_STATUSES = (
        ('todo', 'À Faire'),
        ('doing', 'En Cours'),
        ('done', 'Terminé')
    )

    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=6, choices=ISSUES_TAGS)
    priority = models.CharField(max_length=6, choices=ISSUES_PRIORITIES)
    project_id = models.IntegerField()
    status = models.CharField(max_length=5, choices=ISSUES_STATUSES)
    # Doit compléter la ForeignKey en-dessous
    author_user_key = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    # Doit compléter la ForeignKey en-dessous
    assignee_user_key = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, default=author_user_key, on_delete=models.SET_DEFAULT, related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):

    comment_id = models.IntegerField()
    description = models.CharField(max_length=255)
    # Doit compléter la ForeignKey en-dessous
    author_user_id = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # IMPORTANT : problème est qu'ici issue_id renvoie à Issues et non à Issues.id comme c'est impossible d'après bash
    # de le faire
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
