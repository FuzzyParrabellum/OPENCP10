"""apiSoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from venv import create
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from Troubleshootapp import views


router = routers.SimpleRouter(trailing_slash=False)

router.register(r'projects/?', views.ProjectViewset, basename='projects')
router.register(r'projects/(?P<projects_pk>\d+)/users/?$', \
    views.ContributorViewset, basename='contributors')
router.register(r'projects/(?P<projects_pk>\d+)/issues/?$', \
    views.IssueViewset, basename='issues')
router.register(r'signup/?', views.SignUpViewset, basename="signup")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('projects/<int:projects_pk>/users/<int:users_pk>', \
    views.ContributorViewset.as_view({'get':'retrieve', 'delete':'destroy'}), \
        name='contributors-detail'),
    path('projects/<int:projects_pk>/issues/', 
        views.IssueViewset.as_view({'post':'create'}), name='issues'),
    path('projects/<int:projects_pk>/issues/<int:pk>',
        views.IssueViewset.as_view({'delete':'destroy', 'put':'update'}),
        name='issues_detail'),
    path('projects/<int:projects_pk>/issues/<int:issues_pk>/comments/', 
        views.CommentViewset.as_view({'post':'create', 'get':'list'}), name='comments'),
    path('projects/<int:projects_pk>/issues/<int:issues_pk>/comments/<int:pk>',
        views.CommentViewset.as_view({'delete':'destroy', 'put':'update', 'get':'retrieve'}),
        name='comments_detail'),
    
]