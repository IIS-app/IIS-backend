from rest_framework import serializers
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume, Question

class WinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Win
        fields = ('pk', 'title', 'win', 'win_picture', 'created_date', 'occured_date')

class TargetCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetCompany
        fields = ('pk', 'company_name', 'rank', 'website', 'job_page', 'comments','created_at', 'updated_at')

class CompanyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContacts
        fields = ('pk', 'company', 'name', 'email', 'notes')

class StarrQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarrQuestions
        fields = ('pk', 'question', 'summary', 'situation', 'task', 'action', 'reflection', 'result')

class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ('pk', 'title', 'notes','file')

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('pk', 'title', 'notes', 'file')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('pk', 'question_type', 'question', 'answer')


