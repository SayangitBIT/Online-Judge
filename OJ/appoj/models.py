from django.db import models
from datetime import datetime  
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    total_score = models.FloatField(default = 0)

#through django admin
class Problems(models.Model):
    problem_id = models.AutoField(primary_key = True)
    description = models.CharField(max_length = 255)
    difficulty = models.CharField(max_length = 200)
    solved_status = models.CharField(max_length = 200)
    score = models.FloatField(default = 0)

class TestCases(models.Model):
    problem_id = models.ForeignKey(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE, primary_key = True)
    input = models.CharField(max_length = 200)
    output = models.CharField(max_length = 200)

class Submissions(models.Model):
    submission_id = models.AutoField(primary_key = True)
    problem_id = models.ForeignKey(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE)
    user_id = models.ForeignKey(UserProfile, verbose_name = ('user.id'), on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default = datetime.now, blank = True)