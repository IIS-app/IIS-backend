from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 
from .serializers import WinSerializer, TargetCompanySerializer, CompanyContactsSerializer, StarrQuestionsSerializer, CoverLetterSerializer, ResumeSerializer, QuestionSerializer, ShortPersonalPitchSerializer, LongPersonalPitchSerializer, LinkSerializer, CompanyCommentSerializer, JobCommentSerializer, JobSerializer, SystemQuestionSerializer, UserSerializer, DossierSerializer, DossierDetailSerializer
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume, Question, ShortPersonalPitch, LongPersonalPitch, Links, CompanyComments, JobComments, Job, Dossier, User, SystemQuestion
from .permissions import IsOwner, IsAdminOrReadOnly

# Create views here

class WinView(generics.ListCreateAPIView):
    queryset = Win.objects.all()
    serializer_class = WinSerializer
    permission_classes = (IsAuthenticated)

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

class SystemQuestionIQView(generics.ListCreateAPIView):
    queryset = SystemQuestion.objects.filter(question_type = 'IQ')
    serializer_class = SystemQuestionSerializer
    permission_classes = (IsAdminOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, question_type='IQ')

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user.id, question_type = 'IQ')

class SystemQuestionCQView(generics.ListCreateAPIView):
    queryset = SystemQuestion.objects.filter(question_type = 'CQ')
    serializer_class = SystemQuestionSerializer
    permission_classes = (IsAdminOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, question_type='CQ')

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user.id, question_type = 'CQ')



class MyQuestions(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer 
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)

class ShortPersonalPitchView(generics.ListCreateAPIView):
    queryset = ShortPersonalPitch.objects.all()
    serializer_class = ShortPersonalPitchSerializer
    permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class LongPersonalPitchView(generics.ListCreateAPIView):
    queryset = LongPersonalPitch.objects.all()
    serializer_class = LongPersonalPitchSerializer
    permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class LinksView(generics.ListCreateAPIView):
    queryset = Links.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class CompanyCommentsView(generics.ListCreateAPIView):
    queryset = CompanyComments.objects.all()
    serializer_class = CompanyCommentSerializer
    permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CompanyComments.objects.filter(user=self.request.user)

class JobCommentsView(generics.ListCreateAPIView):
    queryset = JobComments.objects.all()
    serializer_class = JobCommentSerializer
    permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return JobComments.objects.filter(user=self.request.user)

class TargetJobView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

class DossierView(generics.ListCreateAPIView):
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer
    permission_classes = (IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Dossier.objects.filter(user=self.request.user)

class DossierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dossier.objects.all()
    serializer_class = DossierDetailSerializer
    permission_classes = (IsOwner, IsAuthenticated)



class TargetJobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsOwner]

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

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class SystemQuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemQuestion.objects.all()
    serializer_class = SystemQuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id = self.request.user.id())

