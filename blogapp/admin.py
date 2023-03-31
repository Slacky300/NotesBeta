from django.contrib import admin
from . models import *

admin.site.register(UserAccount)
admin.site.register(Subject)
admin.site.register(Module)
admin.site.register(Notes)
admin.site.register(Comment)
admin.site.register(CmntReply)


# Register your models here.
