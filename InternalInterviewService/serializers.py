from rest_framework import serializers
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume

class WinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Win
        fields = ('title', 'win', 'win_picture', 'created_date', 'occured_date', 'id')

class TargetCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetCompany
        fields = ('company_name', 'rank', 'website', 'job_page', 'comments','created_at', 'updated_at', 'id')

class CompanyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContacts
        fields = ('company', 'name', 'email', 'notes', 'id')

class StarrQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarrQuestions
        fields = ('question', 'summary', 'situation', 'task', 'action', 'reflection', 'result', 'id')

class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ('title', 'notes','file', 'id')

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('title', 'notes', 'file', 'id')




