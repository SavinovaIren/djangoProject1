from django.contrib import admin

from goals.models import GoalCategory, Goal, Comment


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
