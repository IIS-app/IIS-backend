from django.contrib import admin
from .models import User, Win, Question, SystemQuestion, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume, Interview, Job, Dossier, Goal

# Register your models here.

admin.site.register(User)
admin.site.register(Win)
admin.site.register(Question)
admin.site.register(TargetCompany)
admin.site.register(CompanyContacts)
admin.site.register(StarrQuestions)
admin.site.register(CoverLetter)
admin.site.register(Resume)
admin.site.register(Interview)
admin.site.register(Job)
admin.site.register(Dossier)
admin.site.register(Goal)
admin.site.register(SystemQuestion)
