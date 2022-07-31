from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.forms import CharField, EmailField
from django.conf import settings
# Create your models here.


class UserManager(BaseUserManager):

    use_in_migrations: True

    def create_user(self, email, password, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, is_staff=True, is_superuser=True)
        return user

class Users(AbstractUser):

    # USER_ID = 0
    user_id = models.IntegerField(primary_key=True)
    # user_id = models.IntegerField(default=0, primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)


    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    # def save(self, *args, **kwargs):
    #     self.user_id = self.user_id + 1
    #     super(Users, self).save(*args, **kwargs)
        
    # def save(self, *args, **kwargs):
    #     self.user_id = self.USER_ID + 1
    #     super(Users, self).save(*args, **kwargs)
    #     print(f"CREATION NOUVEL UTILISATEUR USER_ID EST DE {self.USER_ID}")

    



class Contributors(models.Model):

    CONTRIBUTOR_TYPES = [
        ('author', 'author'),
        ('contributor', 'contributor')
    ]

    user_id = models.IntegerField()
    project_id = models.IntegerField()
    # IIMPORTANT : apparrement choicefield se trouve plutôt sur forms, que faire de l'info?
    # permission = models.ChoiceField()
    permission = models.CharField(choices=CONTRIBUTOR_TYPES, max_length=11)
    role = models.CharField(max_length=255)

    def __str__(self):
        return "Utilisateur {} Projet {}".format(self.user_id, self.project_id)

class Projects(models.Model):

    PROJECT_TYPES = [
        ('back','back-end'),
        ('front', 'front-end'),
        ('ios', 'iOS'),
        ('android', 'Android')
    ]

    project_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(choices=PROJECT_TYPES, max_length=7)
    # Doit compléter la ForeignKey en-dessous
    author_user_key = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_author_name(self):
        author = Users.objects.filter(user_id=self.author_user_key)
        author_name = author.first_name + author.last_name
        return author_name


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
