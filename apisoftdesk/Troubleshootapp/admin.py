from django.contrib import admin
from Troubleshootapp.models import Users, Contributors, Projects, Issues, Comments

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contributors)
admin.site.register(Projects)
admin.site.register(Issues)
admin.site.register(Comments)