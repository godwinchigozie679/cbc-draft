from django.contrib import admin
from e_learning.models.course import Course, Level,  Learning, Prerequisite
from e_learning.models.video import Video
from e_learning.models.user_course import UserCourse, UserModule
from e_learning.models.course_modules import Modulee
from e_learning.models.course_review import Review
from e_learning.models.sector import Sector, SubSector
from e_learning.models.quiz import Quiz, Question, Answer, Result


class SubSectorAdmin(admin.TabularInline):
    model = SubSector

class SectorAdmin(admin.ModelAdmin):
    inlines = [
        SubSectorAdmin,
    ]



# Combining Module and Video to be Inline

class VideoAdmin(admin.TabularInline):
    model = Video
    

class ModuleeAdmin(admin.ModelAdmin):
    inlines=[VideoAdmin]
    
    list_filter = ['course']
    search_fields = ('course',)
    
    class Meta:
        model = Modulee
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

# For Course Filter   
# class CourseAdmin(admin.ModelAdmin):
    
    
class RequirementAdmin(admin.TabularInline):
    model = Prerequisite
    
class LearningAdmin(admin.TabularInline):
    model = Learning
    


class CourseDataAdmin(admin.ModelAdmin):
    inlines = [
                RequirementAdmin,
        LearningAdmin,        
            ]
    
    list_display = ["name", "get_price", "get_discount", "active",'author',]
    search_fields = ('course',)
    
    list_filter = ['sector', 'active', 'author',]
    
    def get_discount(self, course):
        return f'{course.percentage_discount}%'
    
    def get_price(self, course):
        return f'$ {course.price}'


    
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM  
# Combining Quiz, Questions and Answer to be Tabular

class AnswerAdmin(admin.TabularInline):
    model = Answer
    

class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerAdmin]
    
    # search_fields = ('quiz', 'course',)
    
    list_filter = ['quiz']
    
    class Meta:
        model = Question
   
#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM 

# Quiz User Default User
class QuizTakerResultAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(QuizTakerResultAdmin, self).get_changeform_initial_data(request)
        get_data['user'] = request.user.pk
        return get_data

admin.site.register(Course, CourseDataAdmin)
# admin.site.register()
# Quiz
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result, QuizTakerResultAdmin)
# admin.site.register(Course,CourseAdmin )
admin.site.register(Modulee, ModuleeAdmin)
admin.site.register(Video, )
admin.site.register(UserCourse)
admin.site.register(UserModule)
admin.site.register(Review)
admin.site.register(Sector, SectorAdmin)
admin.site.register(SubSector)
admin.site.register(Level)