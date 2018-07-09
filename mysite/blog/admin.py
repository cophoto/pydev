from django.contrib import admin
from blog import models

# Register your models here.
class blogadmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp')

admin.site.register(models.BlogPost, blogadmin)
