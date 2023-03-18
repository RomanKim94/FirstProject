from django.contrib import admin
from .models import Person, Testing, Trying, Question


class PersonAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'age', 'sex', 'username')
	search_fields = ('first_name', 'last_name', 'username')
	list_editable = ('age', 'sex')


class QuestionAdmin(admin.ModelAdmin):
	list_display = ('text', 'correct_answer', 'test')
	search_fields = ('text', )
	list_filter = ('test', )


@admin.register(Testing)
class TestAdmin(admin.ModelAdmin):
	list_display = ('title', )
	search_fields = ('title', )


@admin.register(Trying)
class TryingAdmin(admin.ModelAdmin):
	list_display = ('person', 'test', 'update_time', 'mark_percents', )
	list_filter = ('person', 'test')


admin.site.register(Person, PersonAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Testing, TestAdmin)
# admin.site.register(Trying, TryingAdmin)

