from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Comment)
admin.site.register(Item)
admin.site.register(DailyPuzzle)
admin.site.register(PracticePuzzle)
admin.site.register(Guess)
admin.site.register(ItemImage)