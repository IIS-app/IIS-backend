from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 
from .serializers import WinSerializer, TargetCompanySerializer, CompanyContactsSerializer, StarrQuestionsSerializer, CoverLetterSerializer, ResumeSerializer, QuestionSerializer, ShortPersonalPitchSerializer, LongPersonalPitchSerializer, LinkSerializer, CompanyCommentSerializer, JobCommentSerializer
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume, Question, ShortPersonalPitch, LongPersonalPitch, Links, CompanyComments, JobComments
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
    queryset = Question.objects.filter(question_type = 'IQ')
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, question_type = 'IQ')

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user.id, question_type='IQ')

class CompanyQuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.filter(question_type = 'CQ')
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, question_type='CQ')

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user.id, question_type = 'CQ')

class ShortPersonalPitchView(generics.ListCreateAPIView):
    queryset = ShortPersonalPitch.objects.all()
    serializer_class = ShortPersonalPitchSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class LongPersonalPitchView(generics.ListCreateAPIView):
    queryset = LongPersonalPitch.objects.all()
    serializer_class = LongPersonalPitchSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class LinksView(generics.ListCreateAPIView):
    queryset = Links.objects.all()
    serializer_class = LinkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class CompanyCommentsView(generics.ListCreateAPIView):
    queryset = CompanyComments.objects.all()
    serializer_class = CompanyCommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CompanyComments.objects.filter(user=self.request.user)

class JobCommentsView(generics.ListCreateAPIView):
    queryset = JobComments.objects.all()
    serializer_class = JobCommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return JobComments.objects.filter(user=self.request.user)

class CompanyCommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyComments.objects.all()
    serializer_class = CompanyCommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class JobCommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobComments.objects.all()
    serializer_class = JobCommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class ShortPersonalPitchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShortPersonalPitch.objects.all()
    serializer_class = ShortPersonalPitchSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class LongPersonalPitchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LongPersonalPitch.objects.all()
    serializer_class = LongPersonalPitchSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Links.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated, IsOwner]

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

