from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50,unique=True)
    image=models.FileField(upload_to='media/',default='image.jpeg')

    description=models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name=models.CharField(max_length=50,unique=True)
    subject= models.ForeignKey('Subject', related_name='topic', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    name=models.CharField(max_length=50)
    basic_theory=models.TextField()
    topic=models.ForeignKey('Topic',related_name='chapter',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Question(models.Model):
    question=models.TextField()
    option1=models.CharField(max_length=50)
    option2=models.CharField(max_length=50)
    option3=models.CharField(max_length=50)
    option4=models.CharField(max_length=50)
    ans=models.TextField(max_length=50)
    chapter=models.ForeignKey('Chapter',related_name='question',on_delete=models.CASCADE)

    def __str__(self):
        return self.question

