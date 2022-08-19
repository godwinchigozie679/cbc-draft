from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from e_learning.models.course import Course
from e_learning.models.course_modules import Modulee
from src import settings   
import random
    



# Create your models here.
class Quiz(models.Model):
    topic = models.CharField(max_length=225)
    slug = models.SlugField(blank=True)
    quiz_serial_number = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_course')
    course_module = models.ForeignKey(Modulee, on_delete=models.CASCADE, related_name= 'course_module_quiz')
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text='duration of the quiz in minute')
    required_score_to_pass = models.IntegerField(help_text='score in %')
      
    
    def get_questions(self):
        questions = list(self.question_to_quiz.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    class Meta:
        ordering = ['course_module']
        
    
    def get_absolute_url(self):
        return reverse("quiz", kwargs={'slug': self.slug, 'pk': self.pk}) 
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.course}|>{self.course_module} |> {self.topic}'
    
    
class Question(models.Model):
    question = models.CharField(max_length=250)        
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question_to_quiz')    
    created = models.DateTimeField(auto_now_add=True)  
    
    class Meta:
        ordering = ['quiz', 'question']
    
    def get_answers(self):
        return self.answer_to_question.all()
    
    def __str__(self):
        return f'{self.question}>>{self.quiz}'   
    
     
    
class Answer(models.Model):     
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_to_question')
    answer = models.CharField(blank=True, max_length=250)      
    correct = models.BooleanField(default=False)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    created = models.DateTimeField(auto_now_add=True)  
       
        
    def __str__(self):
        return f'{self.question}>>{self.answer}>>{self.correct}' 
    
    
class Result(models.Model):    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_result')   
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='quiz_attempter',)   
    score = models.FloatField(default=0)
    module = models.ForeignKey(Modulee, on_delete=models.CASCADE, related_name='course_q_module',)
    created = models.DateTimeField(auto_now_add=True,)  
       
        
    def __str__(self):
        return f'{self.quiz}>> {self.user}>> {self.score}>> {self.pk}'