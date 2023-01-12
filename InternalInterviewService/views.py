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
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, KeepTogether, PageBreak, Table, TableStyle
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
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# Generate a pdf with dossier

@csrf_exempt
def generate_pdf(dossier):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add the title to the PDF as a page header
    page_title_style = ParagraphStyle(name='title', fontName='Helvetica', fontSize=20, wordWrap=True, leading=14, alignment=TA_CENTER)
    title = dossier.title
    elements.append(Paragraph(title, styles["Heading1"]))

    # STARR stories
    if dossier.starrs:
        elements.append(Paragraph("STARR stories", styles["Heading2"]))
        data=[]
        
        data.append(["Question", "Summary", "Situation", "Task", "Action", "Reflection", "Result"])

        # elements.append(KeepTogether(t))


        cell_style = ParagraphStyle(name='test', fontName='Helvetica', fontSize=12, wordWrap=True, leading=14, alignment=TA_CENTER)

        for starr in dossier.starrs.all():
            data.append([Paragraph(starr.question), Paragraph(starr.summary), Paragraph(starr.situation), Paragraph(starr.task), Paragraph(starr.action), Paragraph(starr.reflection), Paragraph(starr.result)])
        t=Table(data, colWidths=[1.07142857*inch]*len(data[0]))

        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.gray),
                               ('TEXTCOLOR',(0,0),(-1,-1),colors.whitesmoke),
                               ('ALIGN',(0,0),(-1,-1),'CENTER'),
                               ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
                               ('FONTSIZE', (0,0), (-1,-1), 12),
                               ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                               ('BACKGROUND',(0,0),(0,-1),colors.beige),
                               ('GRID',(0,0),(-1,-1),1,colors.black),]))
        elements.append(KeepTogether(t))
    

    # Wins
    if dossier.wins:
        data=[]
        elements.append(Paragraph("Wins", styles["Heading2"]))
        data.append(["Win Title", "Win"])
        for win in dossier.wins.all():
            data.append([Paragraph(win.title), Paragraph(win.win)])
        t=Table(data, colWidths=[3.75*inch]*len(data[0]))
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.gray),
                               ('TEXTCOLOR',(0,0),(-1,-1),colors.whitesmoke),
                               ('ALIGN',(0,0),(-1,-1),'CENTER'),
                               ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
                               ('FONTSIZE', (0,0), (-1,-1), 14),
                               ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                               ('BACKGROUND',(0,0),(0,-1),colors.beige),
                               ('GRID',(0,0),(-1,-1),1,colors.black)]))
        elements.append(KeepTogether(t))



    # Questions
    if dossier.questions:
        data=[]
        elements.append(Paragraph("Questions", styles["Heading2"]))
        data.append(["Question", "Answer"])
        for question in dossier.questions.all():
            data.append([Paragraph(question.question), Paragraph(question.answer)])
        t=Table(data, colWidths=[3.75*inch]*len(data[0]))
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.gray),
                               ('TEXTCOLOR',(0,0),(-1,-1),colors.whitesmoke),
                               ('ALIGN',(0,0),(-1,-1),'CENTER'),
                               ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
                               ('FONTSIZE', (0,0), (-1,-1), 14),
                               ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                               ('BACKGROUND',(0,0),(0,-1),colors.beige),
                               ('GRID',(0,0),(-1,-1),1,colors.black)]))
        elements.append(KeepTogether(t))
    

    # Build the PDF
    doc.build(elements)

    # Get the value of the BytesIO buffer
    pdf_file = buffer.getvalue()
    buffer.close()
    
    # Save the PDF to AWS S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
    bucket_name = os.environ['AWS_STORAGE_BUCKET_NAME']

    generated_file_name = "generated_dossiers/generated_dossier_%s.pdf" % dossier.id

    s3.put_object(Bucket= bucket_name, Key=generated_file_name, Body=pdf_file)

    return generated_file_name
    
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
    # breakpoint()
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

        # cover_letter_file = BytesIO(cover_letter_s3_file)

        # resume_file = BytesIO(resume_s3_file)


        # breakpoint()
        # Open the generated pdf using pdfrw

        pdf_pages = pdfrw.PdfReader(pdf_s3_file).pages
        resume_pages = pdfrw.PdfReader(resume_s3_file).pages
        cover_letter_pages = pdfrw.PdfReader(cover_letter_s3_file).pages

        new_pdf = pdfrw.PdfWriter()

        # Add the pages from the input PDFs
        new_pdf.addpages(pdf_pages)
        new_pdf.addpages(resume_pages)
        new_pdf.addpages(cover_letter_pages)

        # breakpoint()
        # # Use pdfrw's merge function to combine the three pdfs
        # merger = pdfrw.PageMerge()
        # for page in pdf_pages:
        #     merger.add(page)
        # for page in resume_pages:
        #     merger.add(page)
        # for page in cover_letter_pages:
        #     merger.add(page)
        # # pdf_pages = merger.render()

        # # Save the combined pdf
        # new_pdf.write('final_dossier.pdf')

        new_pdf_bytes = io.BytesIO()
        new_pdf.write(new_pdf_bytes)
        new_pdf_bytes.seek(0)


        # breakpoint()

        # Save the PDF to AWS S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
        bucket_name = os.environ['AWS_STORAGE_BUCKET_NAME']

        file_name = os.path.join("final_dossiers", "final_dossier_%s.pdf" % dossier.id)


        s3.put_object(Bucket= bucket_name, Key=file_name, Body=new_pdf_bytes.getvalue())

        # breakpoint()
        
    # if resume.resume_file.name and not cover_letter.cover_letter_file.name:
    #     file_name_pdf = generated_pdf_file_name

    #     file_name_resume = resume.resume_file.name

    #     # Attempt to retrieve the file from S3
    #     pdf_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_pdf)['Body']

    #     pdf_file = generate_pdf(dossier)
    #     resume_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_resume)['Body']

    #     # Open the generated pdf using pdfrw
    #     # breakpoint()
    #     pdf_pages = pdfrw.PdfReader(pdf_s3_file).pages
    #     resume_pages = pdfrw.PdfReader(resume_s3_file).pages
    #     new_pdf = pdfrw.PdfWriter()
    #     # Add the pages from the input PDFs
    #     new_pdf.addpages(pdf_pages)
    #     new_pdf.addpages(resume_pages)

    #     # Use pdfrw's merge function to combine the two pdfs
    #     pdf_pages = pdfrw.PageMerge(pdf_pages[0]).add(resume_pages[0]).render()

    #     # Save the combined pdf
    #     new_pdf.write('dossier.pdf')
    # if cover_letter.cover_letter_file.name and not resume.resume_file.name:
    #     file_name_pdf = generated_pdf_file_name
    #     breakpoint()
    #     file_name_cover_letter = dossier.cover_letter.cover_letter_file.name

    #     # Attempt to retrieve the file from S3
    #     pdf_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_pdf)['Body']

    #     cover_letter_s3_file = s3.get_object(Bucket=bucket_name, Key=file_name_cover_letter)['Body']

    #     # Open the generated pdf using pdfrw
    #     # breakpoint()
    #     pdf_pages = pdfrw.PdfReader(pdf_s3_file).pages
    #     cover_letter_pages = pdfrw.PdfReader(cover_letter_s3_file).pages
    #     new_pdf = pdfrw.PdfWriter()
    #     # Add the pages from the input PDFs
    #     new_pdf.addpages(pdf_pages)
    #     new_pdf.addpages(cover_letter_pages)

    #     # Use pdfrw's merge function to combine the two pdfs
    #     pdf_pages = pdfrw.PageMerge(pdf_pages[0]).add(cover_letter_pages[0]).render()

    #     # Save the combined pdf
    #     new_pdf.write('dossier.pdf')

    # # Open the PDF file in binary mode
    # with open('dossier.pdf', 'rb') as f:
    #     # Create an HttpResponse object with the PDF file's contents
    #     response = HttpResponse(f.read(), content_type='application/pdf')
    #     response['Content-Disposition'] = 'inline; filename=pdf'

        file_name = "final_dossiers/final_dossier_%s.pdf" % dossier.id

        final_dossier_pdf_file = s3.get_object(Bucket=bucket_name, Key=file_name)['Body']

        # breakpoint()

        response = HttpResponse(final_dossier_pdf_file, content_type='application/pdf')            
        response['Content-Disposition'] = f'attachment; filename="final_dossier.pdf"'

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
