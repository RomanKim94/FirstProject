from django.contrib import admin
from .models import Person


class PersonAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'age', 'sex', 'username')
	search_fields = ('first_name', 'last_name')
	list_editable = ('age', 'sex')


admin.site.register(Person, PersonAdmin)
