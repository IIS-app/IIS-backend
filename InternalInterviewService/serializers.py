from rest_framework import serializers
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume

class WinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Win
        fields = ('title', 'win', 'win_picture', 'created_date', 'occured_date')

class TargetCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetCompany
        fields = ('company_name', 'rank', 'website', 'job_page', 'comments','created_at', 'updated_at')

class CompanyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContacts
        fields = ('company', 'name', 'email', 'notes')

class StarrQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarrQuestions
        fields = ('question', 'summary', 'situation', 'task', 'action', 'reflection', 'result')

class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ('title', 'notes','file')

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('title', 'notes', 'file')




