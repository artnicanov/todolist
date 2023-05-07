from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.models import User


@admin.register(User)
class CreateUserAdmin(UserAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name')  # поля для отображения в админке
	search_fields = ('username', 'email', 'first_name', 'last_name')  # поля по которым проиводят поиск
	readonly_fields = ('last_login', 'date_joined')  # поля, которые нельзя редактировать

	# блоки с информацией о пользователе
	fieldsets = (
		("Учетка", {'fields': ('username', 'password')}),
		("Персональная информация", {'fields': ('email', 'first_name', 'last_name')}),
		("Разрешения", {'fields': ('is_active', 'is_staff', 'is_superuser')}),
		("Даты активности", {'fields': ('last_login', 'date_joined')}),
	)

# приложение которое не нужно показывать в админке
admin.site.unregister(Group)
