from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Admin, Course, Video, Article, Interaction, Recommendation

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'created_at', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('created_at',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Video)
admin.site.register(Article)
admin.site.register(Interaction)
admin.site.register(Recommendation)