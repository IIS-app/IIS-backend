from rest_framework import serializers
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume, Question, ShortPersonalPitch, LongPersonalPitch, Links, CompanyComments, JobComments, Job, User, Dossier

class WinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Win
        fields = ('pk', 'title', 'win', 'win_picture', 'created_at', 'updated_at', 'draft',)

class TargetCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetCompany
        fields = ('pk', 'company_name', 'rank', 'website', 'job_page', 'comments','created_at', 'updated_at')

class CompanyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContacts
        fields = ('pk', 'company', 'name', 'email', 'notes', 'created_at', 'updated_at')

class StarrQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarrQuestions
        fields = ('pk', 'question', 'summary', 'situation', 'task', 'action', 'reflection', 'result', 'created_at', 'updated_at', 'draft',)

class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ('pk', 'title', 'notes','file', 'created_at', 'updated_at', 'draft',)

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('pk', 'title', 'notes', 'file', 'created_at', 'updated_at')

class ShortPersonalPitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortPersonalPitch
        fields = ('pk', 'title', 'pitch', 'created_at', 'updated_at', 'draft',)

class LongPersonalPitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongPersonalPitch
        fields = ('pk', 'title', 'pitch', 'created_at', 'updated_at', 'draft',)

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = ('pk', 'title', 'link', 'created_at', 'updated_at')
    


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('pk','question', 'answer', 'created_at', 'updated_at', 'draft',)
        read_only_fields = ('question_type', )


class CompanyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyComments
        fields = ( 'pk', 'company', 'notes', 'important_date', 'contact', 'created_at', 'updated_at')
    

class JobCommentSerializer(serializers.ModelSerializer):
    class meta:
        model = JobComments
        fields = ('pk', 'job', 'notes', 'important_date', 'created_at', 'updated_at')

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('pk', 'title', 'notes', 'job_listing', 'company', 'created_at', 'updated_at')

class SystemQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('pk', 'question', 'created_at', 'updated_at')
        read_only_fields = ('question_type', )
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'codename', 'linkedin', 'github', 'codepen', 'portfolio', 'personal_pitch', 'id')

class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields = ('title', 'job', 'resume', 'cover_letter', 'starrs', 'questions', 'wins', 'created_at', 'updated_at', 'draft',)

