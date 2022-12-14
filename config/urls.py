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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls')),
    path('wins/', views.WinView.as_view(), name='win-list'),
    path('wins/<int:pk>', views.WinDetail.as_view(), name='win-detail'),
    path('target-compay/', views.TargetCompanyView.as_view(), name='target-co-list'),
    path('target-company/<int:pk>', views.TargetCompanyDetail.as_view(), name='target-co-detail'),
    path('target-company/contacts', views.CompanyContactsView.as_view(), name='contact-list'),
    path('starr-stories/', views.StarrQuestionsView.as_view(), name='starr-stories'),
    path('starr-stpries/<int:pk>', views.StarrQuestionsDetial.as_view(), name='starr-stories-detail'),
    path('cover-letter/', views.CoverLetterView.as_view(), name='cover-letter'),
    path('cover-letter/<int:pk>', views.CoverLetterDetail.as_view(), name='cover-letter-detail'),
    path('resume/', views.ResumeView.as_view(), name='resume'),
    path('resume/<int:pk>', views.ResumeDetail.as_view(), name='resume-detail'),
]
