from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
# from django.db.models.fields import DateTimeField, DateField


# Create your models here.

# Create custom user manager here
class UserManager(BaseUserManager):
  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    if not password:
        raise ValueError('Please provide a password')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user

# Create User model here
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    codename = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    codepen = models.URLField(null=True, blank=True)
    portfolio = models.URLField(null=True, blank=True)
    personal_pitch = models.TextField(null=True, blank=True, max_length=1000)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'codename']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    # personal_pitch
    # links


class TargetCompany(models.Model):
    RANK_CHOICES=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=155)
    rank = models.CharField(choices=RANK_CHOICES, null=True, blank=True,max_length=10)
    website = models.URLField()
    job_page = models.URLField()
    comments = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CompanyContacts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    company = models.ForeignKey(TargetCompany, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class StarrQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=500)
    summary = models.TextField(max_length=1000, null=True, blank=True)
    situation = models.TextField(max_length=500, null=True, blank=True)
    task = models.TextField(max_length=500, null=True, blank=True)
    action = models.TextField(max_length=500, null=True, blank=True)
    reflection = models.TextField(max_length=500, null=True, blank=True)
    result = models.TextField(max_length=500, null=True, blank=True)


class CoverLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    file = models.FileField(upload_to='coverletter')

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    file = models.FileField(upload_to='resume')
