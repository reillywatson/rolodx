from main.models import Professional, Category, ProfessionalCategory, Service, Review, ProfessionalReview, UserProfessional, UserProfile
from django.contrib import admin

# Kept in the same order as models.py
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Professional)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(ProfessionalReview)
admin.site.register(ProfessionalCategory)
admin.site.register(UserProfessional)
