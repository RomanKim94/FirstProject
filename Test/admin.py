from django.contrib import admin
from .models import Person


class PersonAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'age', 'sex', 'login')
	search_fields = ('full_name',)
	list_editable = ('age', 'sex')


admin.site.register(Person, PersonAdmin)
