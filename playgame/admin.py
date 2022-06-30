
from django.contrib import admin
from fluent_contents.admin import PlaceholderFieldAdmin
# Register your models here.
from .models import coursedetails, coursename, rom,topic,message,Article
admin.site.register(rom)
admin.site.register(topic)
admin.site.register(message)

admin.site.register(coursename)

admin.site.register(coursedetails)
class ArticlesAdmin(PlaceholderFieldAdmin):
    pass

admin.site.register(Article,ArticlesAdmin)

