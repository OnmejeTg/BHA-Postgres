from django.contrib import admin
from .models import Parent, Pupil, Grade, Staff, feeFirst, feeThird, feeSecond

# Register your models here.

admin.site.register(Parent)
admin.site.register(Pupil)
admin.site.register(Grade)
admin.site.register(Staff)
admin.site.register(feeFirst)
admin.site.register(feeSecond)
admin.site.register(feeThird)
