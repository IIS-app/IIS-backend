from rest_framework import serializers
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume, Question, ShortPersonalPitch, LongPersonalPitch, Links, CompanyComments, JobComments, Job, User, Dossier, SystemQuestion
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
                             
class WinSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = Win
        fields = ('pk', 'title', 'win', 'win_picture', 'created_at', 'updated_at', 'draft', 'tags')

    def update(self, instance, validated_data):
        if "file" in self.initial_data:
            file = self.initial_data.get("file")
            instance.win_picture.save(file.name, file, save=True)
            return instance
        # this call to super is to make sure that update still works for other fields
        return super().update(instance, validated_data)

class TargetCompanySerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = TargetCompany
        fields = ('pk', 'company_name', 'rank', 'website', 'job_page', 'comments','created_at', 'updated_at', 'tags')

class CompanyContactsSerializer(serializers.ModelSerializer):
    company_title = serializers.CharField(source = 'company.company_title', required=False)
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = CompanyContacts
        fields = ('pk', 'company', 'name', 'email', 'notes', 'created_at', 'updated_at')

class StarrQuestionsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = StarrQuestions
        fields = ('pk', 'question', 'summary', 'situation', 'task', 'action', 'reflection', 'result', 'created_at', 'updated_at', 'draft', 'tags')

class CoverLetterSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = CoverLetter
        fields = ('pk', 'title', 'notes','cover_letter_file', 'created_at', 'updated_at', 'draft', 'tags')

    def update(self, instance, validated_data):
        if "file" in self.initial_data:
            file = self.initial_data.get("file")
            instance.cover_letter_file.save(file.name, file, save=True)
            return instance
        # this call to super is to make sure that update still works for other fields
        return super().update(instance, validated_data)

class ResumeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = Resume
        fields = ('pk', 'title', 'notes', 'resume_file', 'created_at', 'updated_at', 'tags')

    def update(self, instance, validated_data):
        if "file" in self.initial_data:
            file = self.initial_data.get("file")
            instance.resume_file.save(file.name, file, save=True)
            return instance
        # this call to super is to make sure that update still works for other fields
        return super().update(instance, validated_data)

class ShortPersonalPitchSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = ShortPersonalPitch
        fields = ('pk', 'title', 'pitch', 'created_at', 'updated_at', 'draft', 'tags')

class LongPersonalPitchSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = LongPersonalPitch
        fields = ('pk', 'title', 'pitch', 'created_at', 'updated_at', 'draft',  'tags')

class LinkSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = Links
        fields = ('pk', 'title', 'link', 'created_at', 'updated_at')

class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = Question
        fields = ('pk','question', 'answer', 'created_at', 'updated_at', 'draft', 'tags', 'question_type')

class SystemQuestionSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = SystemQuestion
        fields = ('pk', 'question', 'tags', 'question_type')

class CompanyCommentSerializer(serializers.ModelSerializer):
    company_title = serializers.CharField(source='company.company_name', required=False)
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = CompanyComments
        fields = ( 'pk', 'company', 'company_title', 'notes', 'important_date', 'contact', 'created_at', 'updated_at')
    
class JobCommentSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', required=False)
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class meta:
        model = JobComments
        fields = ('pk', 'job', 'job_title', 'notes', 'important_date', 'created_at', 'updated_at')

class JobSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    company_title = serializers.CharField(source='company.company_name', required=False)
    dossier_title = serializers.CharField(source='dossier.title', required=False)
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = Job
        fields = ('pk', 'title', 'notes', 'job_listing', 'company', 'company_title', 'dossier', 'dossier_title', 'created_at', 'updated_at', 'tags')
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'codename', 'linkedin', 'github', 'codepen', 'portfolio', 'personal_pitch', 'id')

class DossierSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = Dossier
        fields = ('title', 'job', 'resume', 'cover_letter', 'starrs', 'questions', 'wins', 'created_at', 'updated_at', 'draft', 'tags', 'id')

class DossierDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    company = serializers.CharField(source='job.company', required=False)
    resume_title = serializers.CharField(source='resume.title', required=False)
    cover_letter_title = serializers.CharField(source='cover_letter.title', required=False)
    starr_titles = serializers.SerializerMethodField(required=False)
    win_titles = serializers.SerializerMethodField(required=False)
    question_titles = serializers.SerializerMethodField(required=False)
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")

    def get_starr_titles(self, obj):
        starr_titles = []
        for starr in obj.starrs.all():
            starr_titles.append({'id': starr.id, 'title': starr.question})
        return starr_titles

    def get_win_titles(self, obj):
        win_titles = []
        for win in obj.wins.all():
            win_titles.append({'id': win.id, 'title': win.title})
        return win_titles

    def get_question_titles(self, obj):
        question_titles = []
        for question in obj.questions.all():
            question_titles.append({'id': question.id, 'title': question.question, 'type': question.question_type})
        return question_titles

    class Meta:
        model = Dossier
        fields = ['id', 'title', 'company', 'starrs','starr_titles', 'resume', 'resume_title', 'cover_letter','cover_letter_title', 'questions', 'question_titles', 'wins', 'win_titles', 'user', 'created_at', 'updated_at', 'draft', 'tags']
        read_only_fields = ['job_title','starr_titles','win_titles']

class ResumeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(required=False, format="%m/%d/%Y %I:%M %p")
    class Meta:
        model = Resume
        fields = ('pk', 'title', 'notes', 'file', 'created_at', 'updated_at', 'tags')

