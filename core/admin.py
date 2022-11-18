from django.contrib import admin
from .models import Parent, Pupil, Grade, Staff, feeFirst, feeThird, feeSecond, Announcement


admin.site.site_header = 'BHA Admin'
admin.site.site_title = 'BHA Admin Area'
admin.site.index_title = 'Welcome to the BHA admin Area'
# Register your models here.

admin.site.register(Parent)
admin.site.register(Pupil)
admin.site.register(Grade)
admin.site.register(Staff)
admin.site.register(feeFirst)
admin.site.register(feeSecond)
admin.site.register(feeThird)
admin.site.register(Announcement)
