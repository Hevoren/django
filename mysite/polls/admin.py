from django.contrib import admin
from .models import Question, Choice, AdvUser


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


@admin.register(AdvUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'avatar', 'email')
