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

# from Troubleshootapp.views import ContributorViewset, CommentViewset, \
#     ProjectViewset, IssueViewset, SignUpViewset

from Troubleshootapp import views


router = routers.SimpleRouter(trailing_slash=False)

router.register(r'projects/?', views.ProjectViewset, basename='projects')
router.register(r'projects/(?P<projects_pk>\d+)/users/?$', \
    views.ContributorViewset, basename='contributors')
router.register(r'projects/(?P<projects_pk>\d+)/issues/?$', \
    views.IssueViewset, basename='issues')
# router.register(r'projects/(?P<projects_pk>\d+)/users/(?P<users_pk>\d+)/?$', \
#     views.ContributorViewset, basename='contributors-detail')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    # path(r'projects/<projects_pk>/users/<users_pk>/?', \
    # views.ContributorViewset.as_view({'get':'retrieve'}), name='contributors-detail')
    path('projects/<int:projects_pk>/users/<int:users_pk>', \
    views.ContributorViewset.as_view({'get':'retrieve', 'delete':'destroy'}), \
        name='contributors-detail'),
    path('projects/<int:projects_pk>/issues/', \
    views.IssueViewset.as_view({'post':'create'}), \
        name='issues')
    
]

# router = routers.SimpleRouter(trailing_slash=False)

# router.register(r'projects/?', ProjectViewset, basename="projects")

# project_router = routers.NestedSimpleRouter(router, r'projects/?', lookup='projects')
# project_router.register(r'users/?', ContributorViewset, basename='contributors')
# project_router.register(r'issues/?', IssueViewset, basename='issues')
# # router.register(r'^projects/(?P<projects_pk>\d+)/users/?$', ContributorViewset, basename="contributor")
# router.register('Comment', CommentViewset, basename="comment")
# # router.register('projects', ProjectViewset, basename="projects")
# # router.register('Issue', IssueViewset, basename="issue")
# router.register('signup', SignUpViewset, basename="signup")
# # bout de code montrant comment faire un nested router
# # url(r'^libraries/(?P<library_pk>\d+)/books/?$', views.BookViewSet.as_view({'get': 'list'}), name='library-book-list')
# # # Get details of a book in a library
# # url(r'^libraries/(?P<library_pk>\d+)/books/(?P<pk>\d+)/?$', views.BookViewSet.as_view({'get': 'retrieve'}), name='library-book-detail')