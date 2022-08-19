from e_learning.models.course_review import Review
from e_learning.models.course_forms import ReviewForm
from e_learning.models.course import Course
from e_learning.models.course_modules import Modulee
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from e_learning.models.user_course import UserCourse
from django.contrib import messages
from django.db.models import Avg
from e_learning.models.quiz import Quiz, Question, Answer, Result
from django.http import JsonResponse


def course_quiz(request, slug, pk):
    quiz = Quiz.objects.get(slug=slug)
    pk = quiz.pk
        
    context = {
        'quiz': quiz,
        'pk': pk
        }
        
    return render(request, template_name='quiz/quiz.html', context=context)


def course_quiz_data(request, slug, pk):
    quiz = Quiz.objects.get(slug=slug)
    pk = quiz.pk
    
    questions = []
    for q in quiz.get_questions():        
        answers = []        
        for a in q.get_answers():
            answers.append(a.answer)
        questions.append({str(q.question): answers})
    
    return JsonResponse(
        {'data': questions,
         'time': quiz.time,  
         'pk':pk       
         }
    )
    

   
def course_quiz_save(request, slug, pk):
    
    if request.is_ajax():
        questions = []       
        data = request.POST        
        data_ = dict(data.lists())
        
        
        data_.pop('csrfmiddlewaretoken')
        
        quiz = Quiz.objects.get(slug=slug)
        pk=quiz.pk
        user = request.user
               
        for k in data_.keys():                    
            question = Question.objects.filter(question=k, quiz=quiz)            
            for qz in question:
                questions.append(qz.question)                
        
        score = 0
        multiplier = 100/quiz.number_of_questions
        results = []
        correct_answer = 'correct'
                     
        # Getting selected answer 
        for q in questions:            
            answer_selected = request.POST.get(q)
                        
            if answer_selected != "":
                answer_ =[]
                question_answers = Answer.objects.filter(question__question=q, answer=answer_selected)
                for answer in question_answers:
                    correct = answer.correct                    
                    answer_.append(answer.answer)
                
                # main answer
                for answer_m in answer_:
                    answer = answer_m
                    
                if answer_selected == answer_m:
                    if correct == True:
                        score += 1
                        correct_answer = answer_m                   
                else:
                    if correct:
                        correct_answer = answer_m 
                        # print(correct_answer, '.....2')  
                                               
                    correct_answer = answer_m 
                    # print(correct_answer, '.....')       
                results.append({str(q): {'correct_answer': correct_answer, 
                                         'answered': answer_selected, 'pk':pk} 
                                })   
            else:
                results.append({str(q): 'not_answered'})  
               
        score_ = score * multiplier
        
        course = quiz.course
        modules = Modulee.objects.filter(course=course,)  #Logic for next and previous video
        previous_module = quiz.quiz_serial_number
        current_module = previous_module + 1
        for module in modules[previous_module:current_module]:
            module = module
        
        # Create Result
        result_ = Result.objects.filter(user=user, quiz__slug=slug, module=module) # Result instance 
        
        if result_.exists():
            Result.objects.update(quiz=quiz, user=user, score=score_, module=module)
        else:
            # Update Result
            r = Result.objects.create(quiz=quiz, user=user, score=score_, module=module)            
            r.save()
            
            
        
        if score_ >= quiz.required_score_to_pass:            
            return JsonResponse({'passed': True, 'score': score_, 'results': results, 'pass_score':quiz.required_score_to_pass})  
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results, 'pass_score':quiz.required_score_to_pass })     
    
    
   
   
   
   

    