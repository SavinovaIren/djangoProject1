from django.contrib import admin

from goals.models import GoalCategory, Goal, Comment, BoardParticipant, Board


class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated")
    search_fields = ("title",)


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role')
    search_fields = ('board', 'user', 'role')


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'created', 'updated', 'category')
    search_fields = ('title', 'description', 'user')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'created', 'updated', 'goal')
    search_fields = ('text', 'user')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)