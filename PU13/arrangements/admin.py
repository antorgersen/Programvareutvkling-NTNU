from django.contrib import admin
from .models import Challenge, KnitNight, Ads


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('challenge_name', 'rec_user_level', 'created_at', 'created_by')


class KnitAdmin(admin.ModelAdmin):
    list_display = ('knit_name', 'time', 'created_at', 'created_by')


class YarnAdmin(admin.ModelAdmin):
    list_display = ('yarn_name', 'created_at', 'created_by')


admin.site.register(Ads, YarnAdmin)
admin.site.register(KnitNight, KnitAdmin)
admin.site.register(Challenge, ChallengeAdmin)
