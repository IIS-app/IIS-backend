"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from InternalInterviewService import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls')),
    path('wins/', views.WinView.as_view(), name='win-list'),
    path('wins/<int:pk>', views.WinDetail.as_view(), name='win-detail'),
    path('target-jobs/', views.TargetJobView.as_view(), name='job-list'),
    path('target-jobs/<int:pk>', views.TargetJobDetail.as_view(), name = 'job-detail'),
    path('target-company/', views.TargetCompanyView.as_view(), name='target-co-list'),
    path('target-company/<int:pk>', views.TargetCompanyDetail.as_view(), name='target-co-detail'),
    path('target-company/contacts/', views.CompanyContactsView.as_view(), name='contact-list'),
    path('target-company/contacts/<int:pk>', views.CompanyContactsDetail.as_view(), name='contact-detail'),
    path('target-company/comments/', views.CompanyCommentsView.as_view(), name='company-comment'),
    path('starr-stories/', views.StarrQuestionsView.as_view(), name='starr-stories'),
    path('starr-stories/<int:pk>', views.StarrQuestionsDetial.as_view(), name='starr-stories-detail'),
    path('cover-letter/', views.CoverLetterView.as_view(), name='cover-letter'),
    path('cover-letter/<int:pk>', views.CoverLetterDetail.as_view(), name='cover-letter-detail'),
    path('resume/', views.ResumeView.as_view(), name='resume'),
    path('resume/<int:pk>', views.ResumeDetail.as_view(), name='resume-detail'),
    path('personal-pitch/short/', views.ShortPersonalPitchView.as_view(), name='short-personal-pitch'),
    path('personal-pitch/short/<int:pk>', views.ShortPersonalPitchDetail.as_view(), name='short-personal-pitch-detail'),
    path('personal-pitch/long/', views.LongPersonalPitchView.as_view(), name='long-personal-pitch'),
    path('personal-pitch/long/<int:pk>', views.LongPersonalPitchDetail.as_view(), name='long-personal-pitch-detail'),
    path('user/links/', views.LinksView.as_view(), name='links'),
    path('user/links/<int:pk>', views.LinkDetail.as_view(), name='links-detail'),
    path('interview-question/', views.InterviewQuestionView.as_view(), name='interview-question'),
    path('company-question/', views.CompanyQuestionView.as_view(), name='company-question'),
    path('system-question/', views.SystemQuestionView.as_view(), name='system-question'),
    path('system-question/<int:pk>', views.SystemQuestionDetail.as_view, name='system-question-detail'),
    path('interview-question/<int:pk>', views.InterviewQuestionDetail.as_view(), name='interview-question-detail'),
    path('company-question/<int:pk>', views.CompanyQuestionDetail.as_view(), name='company-question-detail'),
    path('user/me<int:pk>', views.UserDetail.as_view(), name='profile'),
    path('dossier/', views.DossierView.as_view(), name='dossier-generic'),
    path('dossier/<int:pk>', views.DossierDetail.as_view(), name='dossier-detail'),
    path('win-picture/<int:pk>', views.WinPictureView.as_view(), name='win-picture')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)