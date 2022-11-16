from django.contrib import admin
from .models import Question, Choice, User, Vote


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'avatar', 'email')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    model = Vote
