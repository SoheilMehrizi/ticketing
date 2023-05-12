from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.user import User, Customer

class CustomUserAdmin(UserAdmin):

    model = User

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        ("Authentication", {
            "fields": (
                'email', 
                'password',
                
            ),
        }),
        ("Permisions", {
            "fields": (
                'is_superuser',
                'is_staff',
                'is_active',
            ),
        }),

        ("Group Permisions", {
            "fields": (
                'groups',
                'user_permissions',
            ),
        }),

        ("Important Dates", {
            "fields": (
                'last_login',)
        }),
    )
    
    add_fieldsets = (
        ("New User", {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_superuser',
                'is_staff', 'is_active')
        }),
        
    )

admin.site.register(Customer)
admin.site.register(User, CustomUserAdmin)