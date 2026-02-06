from django.contrib import admin
# from django.contrib.auth.models import User, Group
from .models import Post, Comment

# Register your models here.
# user, created = User.objects.get_or_create(username="admin_user", defaults={'password': 'admin_password'})
# admin_group, created = Group.objects.get_or_create(name="Admin")
# user.groups.add(admin_group)

#admin user cred: "admin_user", "admin_password"
#test user cred: "new_user", "testpass_123"


admin.site.register(Post)
admin.site.register(Comment)

#username: admin
#email: admin@admin.com
#pass: password
