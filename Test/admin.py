from django.contrib import admin
from .models import Person


class PersonAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'age', 'sex', 'slug')
	search_fields = ('full_name',)
	list_editable = ('age', 'sex')
	prepopulated_fields = {'slug': ('full_name', 'age')}


admin.site.register(Person, PersonAdmin)
