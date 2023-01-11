from django.shortcuts import render
from rest_framework import generics, parsers
from rest_framework.permissions import IsAuthenticated 
from .serializers import WinSerializer, TargetCompanySerializer, CompanyContactsSerializer, StarrQuestionsSerializer, CoverLetterSerializer, ResumeSerializer, QuestionSerializer, ShortPersonalPitchSerializer, LongPersonalPitchSerializer, LinkSerializer, CompanyCommentSerializer, JobCommentSerializer, JobSerializer, SystemQuestionSerializer, UserSerializer, DossierSerializer, DossierDetailSerializer
from .models import Win, TargetCompany, CompanyContacts, StarrQuestions, CoverLetter, Resume, Question, ShortPersonalPitch, LongPersonalPitch, Links, CompanyComments, JobComments, Job, Dossier, User, SystemQuestion
from .permissions import IsOwner, IsAdminOrReadOnly
from django.views.generic.edit import CreateView
from django.core.files.storage import FileSystemStorage
from datetime import datetime

#for pdf generation
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import requests
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import environ
import boto3
import botocore
import pdfrw
from pdfrw import PdfReader
from botocore.exceptions import ClientError

# Generate a pdf with dossier

@csrf_exempt
def generate_pdf(dossier):
    # dosier = dossier.objects
    # Create a new PDF
    pdf = canvas.Canvas('output.pdf')

    # Add the title to the PDF
    pdf.drawString(100, 750, dossier.title)
    # MY STARRS TITLE
    if dossier.starrs:
        pdf.drawString(100, 600, "MY STARRS")
        # textobject = pdf.beginText(dossier.starrs.all())

    # Iterate through the STARR questions and add them to the PDF
    for starr in dossier.starrs.all():
        pdf.drawString(100, 525, starr.question)
        pdf.drawString(100, 526, starr.summary)
        pdf.drawString(100, 527, starr.situation)
        pdf.drawString(100, 528, starr.task)
        pdf.drawString(100, 529, starr.action)
        pdf.drawString(100, 530, starr.reflection)
        pdf.drawString(100, 531, starr.result)

    # Iterate through the questions and add them to the PDF
    for question in dossier.questions.all():
        pdf.drawString(100, 550, question.question)

    # Iterate through the wins and add them to the PDF
    for win in dossier.wins.all():
        pdf.drawString(100, 500, win.title)

    # Save the PDF
    pdf.save()

    # Open the PDF file in binary mode
    with open('output.pdf', 'rb') as f:
        # Read the contents of the PDF file
        pdf_file = f.read()
    
    # Define the S3 bucket and file name
    bucket_name = os.environ['AWS_STORAGE_BUCKET_NAME']
    i = 1
    while os.path.isfile(f'generated_dossier_pdfs/generated_dossier_{i}.pdf'):
        i += 1
    file_name = f'generated_dossier_pdfs/generated_dossier_{i}.pdf'

    # Connect to S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    # Upload the PDF file to S3
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=pdf_file)

    # you may need to return the file_name for next merge function.
    return file_name

@csrf_exempt
def merge_pdf(request, pk):
    # Try to retrieve the Dossier object
    try:
        dossier = Dossier.objects.get(pk=pk)
    except Dossier.DoesNotExist:
        # Return a 404 response if the Dossier object does not exist
        return HttpResponse('Dossier not found', status=404)

    # Generate the pdf containing the user's data
    generated_pdf_file_name = generate_pdf(dossier)

    # Retrieve the resume file from the S3 bucket
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
    bucket_name = os.environ['AWS_STORAGE_BUCKET_NAME']
    # Define the S3 bucket and file name

    resume = dossier.resume
    
    cover_letter = dossier.cover_letter

    # Download the files from S3 and save it to a variable if they exist
    if resume.resume_file.name and cover_letter.cover_letter_file.name:
        file_name_pdf = generated_pdf_file_name
        
        file_name_resume = dossier.resume.resume_file.name

        file_name_cover_letter = dossier.cover_letter.cover_letter_file.name

        # Attempt to retrieve the file from S3
        pdf_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_pdf)['Body']

        resume_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_resume)['Body']

        cover_letter_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_cover_letter)['Body']

        # Open the generated pdf using pdfrw
        # breakpoint()
        pdf_pages = pdfrw.PdfReader(pdf_s3_file).pages
        resume_pages = pdfrw.PdfReader(resume_s3_file).pages
        cover_letter_pages = pdfrw.PdfReader(cover_letter_s3_file).pages
        new_pdf = pdfrw.PdfWriter()
        # Add the pages from the input PDFs
        new_pdf.addpages(pdf_pages)
        new_pdf.addpages(resume_pages)
        new_pdf.addpages(cover_letter_pages)

        # Use pdfrw's merge function to combine the two pdfs
        pdf_pages = pdfrw.PageMerge(pdf_pages[0]).add(resume_pages[0],cover_letter_pages[0]).render()

        # Save the combined pdf
        new_pdf.write('dossier.pdf')
    if resume.resume_file.name and not cover_letter.cover_letter_file.name:
        file_name_pdf = generated_pdf_file_name

        file_name_resume = resume.resume_file.name

        # Attempt to retrieve the file from S3
        pdf_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_pdf)['Body']

        pdf_file = generate_pdf(dossier)
        resume_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_resume)['Body']

        # Open the generated pdf using pdfrw
        # breakpoint()
        pdf_pages = pdfrw.PdfReader(pdf_s3_file).pages
        resume_pages = pdfrw.PdfReader(resume_s3_file).pages
        new_pdf = pdfrw.PdfWriter()
        # Add the pages from the input PDFs
        new_pdf.addpages(pdf_pages)
        new_pdf.addpages(resume_pages)

        # Use pdfrw's merge function to combine the two pdfs
        pdf_pages = pdfrw.PageMerge(pdf_pages[0]).add(resume_pages[0]).render()

        # Save the combined pdf
        new_pdf.write('dossier.pdf')
    if cover_letter.cover_letter_file.name and not resume.resume_file.name:
        file_name_pdf = generated_pdf_file_name

        file_name_cover_letter = dossier.cover_letter.cover_letter_file.name

        # Attempt to retrieve the file from S3
        pdf_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_pdf)['Body']

        cover_letter_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_cover_letter)['Body']

        # Open the generated pdf using pdfrw
        # breakpoint()
        pdf_pages = pdfrw.PdfReader(pdf_s3_file).pages
        cover_letter_pages = pdfrw.PdfReader(cover_letter_s3_file).pages
        new_pdf = pdfrw.PdfWriter()
        # Add the pages from the input PDFs
        new_pdf.addpages(pdf_pages)
        new_pdf.addpages(cover_letter_pages)

        # Use pdfrw's merge function to combine the two pdfs
        pdf_pages = pdfrw.PageMerge(pdf_pages[0]).add(cover_letter_pages[0]).render()

        # Save the combined pdf
        new_pdf.write('dossier.pdf')

    # Open the PDF file in binary mode
    with open('dossier.pdf', 'rb') as f:
        # Create an HttpResponse object with the PDF file's contents
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=pdf'

        return response



# Create views here

class WinView(generics.ListCreateAPIView):
    queryset = Win.objects.all()
    serializer_class = WinSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Win.objects.filter(user=self.request.user)

class WinPictureView(generics.UpdateAPIView):
    queryset = Win.objects.all()
    serializer_class = WinSerializer
    parser_classes = [parsers.FileUploadParser]
    permission_classes = [IsAuthenticated]

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

class CoverLetterFileView(generics.UpdateAPIView):
    queryset = CoverLetter.objects.all()
    serializer_class = CoverLetterSerializer
    parser_classes = [parsers.FileUploadParser]
    permission_classes = [IsAuthenticated]

class ResumeView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeFileView(generics.UpdateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = [parsers.FileUploadParser]
    permission_classes = [IsAuthenticated]

class QuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user.id)

class SystemQuestionView(generics.ListCreateAPIView):
    queryset = SystemQuestion.objects.all()
    serializer_class = SystemQuestionSerializer

    def get_queryset(self):
        return SystemQuestion.objects.all()

class MyQuestions(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer 
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)

class ShortPersonalPitchView(generics.ListCreateAPIView):
    queryset = ShortPersonalPitch.objects.all()
    serializer_class = ShortPersonalPitchSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return ShortPersonalPitch.objects.filter(user=self.request.user)

class LongPersonalPitchView(generics.ListCreateAPIView):
    queryset = LongPersonalPitch.objects.all()
    serializer_class = LongPersonalPitchSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return LongPersonalPitch.objects.filter(user=self.request.user)

class LinksView(generics.ListCreateAPIView):
    queryset = Links.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Links.objects.filter(user=self.request.user)

class CompanyCommentsView(generics.ListCreateAPIView):
    queryset = CompanyComments.objects.all()
    serializer_class = CompanyCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CompanyComments.objects.filter(user=self.request.user)

class JobCommentsView(generics.ListCreateAPIView):
    queryset = JobComments.objects.all()
    serializer_class = JobCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return JobComments.objects.filter(user=self.request.user)

class TargetJobView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

class DossierView(generics.ListCreateAPIView):
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Dossier.objects.filter(user=self.request.user)

class DossierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dossier.objects.all()
    serializer_class = DossierDetailSerializer
    permission_classes = [IsOwner, IsAuthenticated]

class TargetJobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsOwner, IsAuthenticated,]
    
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
