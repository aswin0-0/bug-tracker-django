from django.contrib import admin

# Register your models here.
from .models import bugs_report  # ✅ import your model

# ✅ register the model
admin.site.register(bugs_report)