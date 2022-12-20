from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 
from .serializers import WinSerializer, TargetCompanySerializer, CompanyContactsSerializer, StarrQuestionsSerializer, CoverLetterSerializer, ResumeSerializer, QuestionSerializer
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume, Question
from .permissions import IsOwner

# Create views here

class WinView(generics.ListCreateAPIView):
    queryset = Win.objects.all()
    serializer_class = WinSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Win.objects.filter(user=self.request.user)

class TargetCompanyView(generics.ListCreateAPIView):
    queryset = TargetCompany.objects.all()
    serializer_class = TargetCompanySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return TargetCompany.objects.filter(user=self.request.user)

class CompanyContactsView(generics.ListCreateAPIView):
    queryset = CompanyContacts.objects.all()
    serializer_class = CompanyContactsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CompanyContacts.objects.filter(user=self.request.user)

class StarrQuestionsView(generics.ListCreateAPIView):
    queryset = StarrQuestions.objects.all()
    serializer_class = StarrQuestionsSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return StarrQuestions.objects.filter(user=self.request.user.id)

class CoverLetterView(generics.ListCreateAPIView):
    queryset = CoverLetter.objects.all()
    serializer_class = CoverLetterSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)

class ResumeView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class InterviewQuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    

    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user.id)

class CompanyQuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.filter(question_type = 'CQ')
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user.id)

class WinDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Win.objects.all()
    serializer_class = WinSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class TargetCompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TargetCompany.objects.all()
    serializer_class = TargetCompanySerializer
    permission_classes = [IsAuthenticated, IsOwner]

class CompanyContactsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyContacts.objects.all()
    serializer_class = CompanyContactsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class StarrQuestionsDetial(generics.RetrieveUpdateDestroyAPIView):
    queryset = StarrQuestions.objects.all()
    serializer_class = StarrQuestionsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class CoverLetterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoverLetter.objects.all()
    serializer_class = CoverLetterSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class ResumeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class InterviewQuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.filter(question_type = 'IQ')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class CompanyQuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.filter(question_type = 'CQ')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsOwner]