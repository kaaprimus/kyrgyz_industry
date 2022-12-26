from .models import *
from django.forms import ModelForm, DateTimeInput, TextInput, Textarea, DateInput
from django import forms
from django.contrib.auth.models import User


# News
class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['Title', 'Short_Description', 'Description', 'Date_added', 'Language', 'Gallery']
    
        widgets = {
            'Title' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Название новости","size" : 100, 'required': True}
            ),
            'Short_Description' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "short_description", "placeholder" : "Краткое описание", "size" : 200, 'required': True}
            ),
            'Description' : Textarea(
                attrs = {"class" : "form-control", "id" : "description", "placeholder" : "Полное содержание", 'required': True}
                ),
            'Date_added' : DateTimeInput(
                attrs={'type': 'datetime-local', "class" : "form-control", "id" : "date_created", "required" : False}
                ),
            'Language' : forms.Select(
                attrs={"class": "form-control", 'required': True,  "id" : "language"},
                choices=LanguageChoice.choices
            ),
            'Gallery' : forms.Select(
                attrs={"class": "form-control", 'required': True, "id" : "gallery"}
            )
        }
        
    def check_for_empty(self):
        title = self.cleaned_data.get("Title")
        short_description = self.cleaned_data.get("Short_Description")
        description = self.cleaned_data.get("Description")
        gallery = self.cleaned_data.get("Gallery")
        if title == "" or short_description == "" or description == "" or gallery == "":
            raise forms.ValidationError('Это поле обязательное!')
        return title   
   
# Форма для Галереи
class NewsGalleryForm(ModelForm):
    class Meta:
        model = GalleryNews
        fields = ["Name"]
        widgets = {
            'Name' : TextInput(
                attrs= {"type" : "text", "class" : "form-control", "id" : "name", "placeholder" : "Название  галереи" })
        } 
    def check_for_empty(self):
        name = self.cleaned_data.get("Name")
        if name == "":
            raise forms.ValidationError('Это поле обязательное!')
        return name   
        
# Форма для изображение новости
class NewsImageForm(ModelForm):
    class Meta:
        model = PhotosNews
        fields = ["URL", "Caption", "Gallery"]
        
        widgets = {
            'Caption' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "image-caption", "placeholder" : "Описание изображении", "size" : 110, 'required': False}
            ),
            'Gallery' : forms.Select(
                attrs={"class": "form-control", 'required': True, "id" : "gallery"}
            )
        }
        
# Projects 
class ProjectGalleryForm(ModelForm):
    class Meta:
        model = GalleryProject
        fields = ["Name"]
        widgets = {
            'Name' : TextInput(
                attrs= {"type" : "text", "class" : "form-control", "id" : "name", "placeholder" : "Название  галереи" })
        } 
    def check_for_empty(self):
        name = self.cleaned_data.get("Name")
        if name == "":
            raise forms.ValidationError('Это поле обязательное!')
        return name     
    
class ProjectImageForm(ModelForm):
    class Meta:
        model = PhotosProject
        fields = ["URL", "Caption", "Gallery"]
        
        widgets = {
            'Caption' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "image-caption", "placeholder" : "Описание изображении", "size" : 110, 'required': False}
            ),
            'Gallery' : forms.Select(
                attrs={"class": "form-control", 'required': True, "id" : "gallery"}
            )
        }
# Project Form
class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['Title',  'Description', 'Date_added', 'Language', 'Gallery', 'Category', 'Status']
        widgets = {
            'Title' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Заговолок проекта","size" : 70, 'required': True}
            ),
            'Description' : Textarea(
                attrs = {"class" : "form-control", "id" : "description", "placeholder" : "Полное содержание", 'required': True}
                ),
            'Date_added' : DateTimeInput(
                attrs={'type': 'datetime-local', "class" : "form-control", "id" : "date_created", "required" : False}
                ),
            'Language' : forms.Select(
                attrs={"class": "form-control", 'required': True,  "id" : "language"},
                choices=LanguageChoice.choices
            ),
            'Gallery' : forms.Select(
                attrs={"class": "form-control", 'required': True, "id" : "gallery"}
            ),
            'Category' : forms.Select(
                attrs= {"class": "form-control", 'required': True, "id" : "Category"}
                ), 
            'Status' : forms.Select(
                attrs ={ "class": "form-control", 'required': True, "id" : "Status"},
                choices= Project_Status_Choice.choices
                )
        }

class ProjectCategoryForm(ModelForm):
    class Meta:
        model = ProjectCategory
        fields = '__all__'    

        widgets = {
            'Name' : TextInput(  
                    attrs= {"type" : "text", "class" : "form-control", "id" : "name", "placeholder" : "Название категории"}           
                               )
        } 
        
class ContestForm(ModelForm):
    class Meta:
        model = Contests
        fields = '__all__'
        widgets = {
            'Title' : TextInput(
                    attrs = {"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Название конкурса","size" : 40, 'required': True}
                ),
            'Short_Description' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "short_description", "placeholder" : "Краткое описание", "size" : 110, 'required': True}
            ),
            'Date_added' : DateTimeInput(
                    attrs={'type': 'datetime-local', "class" : "form-control", "id" : "date_created", "required" : False}
                    ),
            'Language' : forms.Select(
                    attrs={"class": "form-control", 'required': True,  "id" : "language"},
                    choices=LanguageChoice.choices
                ),
            'Status' : forms.Select( 
                    attrs={"class": "form-control", 'required': True,  "id" : "language"},
                    choices=LanguageChoice.choices
                    )
            
        }
        

# Vacancies
class VacanciesForm(ModelForm):
    class Meta:
        model = Vacancies
        fields = ['title', 'company', 'Language', 'pub_date', 'description', 'salary', 'positions', 'status', 'email_company']
    
        widgets = {
            'title' : TextInput(
                    attrs = {"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Название вакансии","size" : 110, 'required': True}
                ),
            'company' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "company", "placeholder" : "Название компании","size" : 70, 'required': True}
            ),
            'Language' : forms.Select(
                attrs={"class": "form-control", 'required': True,  "id" : "language"},
                choices=LanguageChoice.choices
            ),
            'pub_date' : DateTimeInput(
                attrs={'type': 'datetime-local', "class" : "form-control", "id" : "date_created", "required" : False}
                ),
            'description' : Textarea(
                attrs = {"class" : "form-control", "id" : "description", "placeholder" : "Полное содержание", 'required': True}
                ),
            'salary' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "salary", "placeholder" : "Оклад","size" : 70, 'required': True}
            ),
            'positions' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "positions", "placeholder" : "Должность","size" : 70, 'required': True}
            ),
            'status' : forms.Select(
                attrs ={ "class": "form-control", 'required': True, "id" : "Status"},
                choices= Vacancy_Status_Choice.choices
                ),
            'email_company' : TextInput(
                attrs = {"type" : "mail", "class" : "form-control", "id" : "email_company", "placeholder" : "Почта компании", "size" : 60, 'required': True}
            ),
        }
        

# Форма для профиля   
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', "id" : "username", "placeholder" : "Введите Имя Пользователя"}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', "id" : "email", "placeholder" : "Введите E-mail"}))

    class Meta:
        model = User
        fields = ['username', 'email']
        
    
# Сотрудники    
class ManagementForm(forms.ModelForm):
    full_name = forms.CharField(max_length=40, required=True, widget=forms.TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "fullname", "placeholder" : "Введите ФИО Сотрудника", "size" : 40}
    ))
    position = forms.CharField(max_length=70, required=True, widget=forms.TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "position", "placeholder" : "Введите Должность", "size" : 70}
    ))
    
    date_birth = forms.DateField(required=True, widget= DateInput(
                    attrs = {"type" : "date", "class" : "form-control", "id" : "date_birth"}
                ))
    mail_link = forms.CharField(max_length=2080, required=False, widget=forms.TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "mail_link", "placeholder" : "Введите ссылку", "size" : 2080}
    ))

    instagram_link = forms.CharField(max_length=2080, required=False, widget=forms.TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "instagram_link", "placeholder" : "Введите ссылку", "size" : 2080}
    ))

    facebook_link = forms.CharField(max_length=2080, required=False, widget=forms.TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "fasebook_link", "placeholder" : "Введите ссылку", "size" : 2080}
    ))
    
    about = forms.Textarea(attrs = {"class" : "form-control", "id" : "about", "placeholder" : "Биография",'required': True})
    
    language = forms.CharField(max_length=10,
                                widget= forms.Select(
                                        attrs={"class" : "form-control", "id" : "language"},
                                        choices=LanguageChoice.choices
                                    )
                            )
    
    class Meta:
        model = Management
        fields = '__all__'

    def check_for_empty(self):
        full_name = self.cleaned_data.get("full_name")
        position = self.cleaned_data.get("position")

        if full_name == "" == "" or position == "":
            raise forms.ValidationError('Это поле обязательное!')
        return full_name 
        
        
class HotNewsGalleryForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "name", "placeholder" : "Введите название галереи", "size" : 50}
    ))
    class Meta:
        model = HotNewsGallery
        fields = '__all__'

class HotNewsImageForm(forms.ModelForm):
    caption = forms.CharField(max_length=70, required=True, widget=TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "caption", "placeholder" : "Введите название фотографии", "size" : 70}
    ))
    gallery = forms.ModelChoiceField(queryset=HotNewsGallery.objects.all(), 
                                     widget=forms.Select(attrs={"class" : "form-control", "id" : "gallery"}))
                    
    class Meta:
        model = HotNewsPhoto
        fields = '__all__'

class HotNewsForm(forms.ModelForm):
    title = forms.CharField(max_length=150, required=True, widget=TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Введите название новости", "size" : 150}
    ))
    short_description = forms.CharField(max_length=220, required=True, widget=TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "short_description", "placeholder" : "Введите краткое описание", "size" : 220}
    ))
    
    description = forms.Textarea(
       
        )
    Language = forms.ChoiceField(
                                choices=LanguageChoice.choices,
                                widget= forms.Select(
                                        attrs={"class" : "form-control", "id" : "language"}
                                    ),
                                required=True
                            )
    pub_date = forms.DateField(required=False, 
                               widget=DateInput(
                                   attrs={"type" : "date", "class" : "form-control", "id" : "pub_date"}
                                   )
                               )
    gallery = forms.ModelChoiceField(queryset=HotNewsGallery.objects.all(), 
                                     widget=forms.Select(attrs={"class" : "form-control", "id" : "gallery"}))
    class Meta:
        model = HotNews
        fields = '__all__'


class InterviewsForm(ModelForm):
    class Meta:
        model = Interviews
        fields = ['title', 'link']
    
    title = forms.CharField(max_length=80, required=True, widget=TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Введите название ссылки", "size" : 80}
    ))
    
    link = forms.CharField(max_length=2080, required=True, widget=TextInput(
        attrs={"type" : "text", "class" : "form-control", "id" : "link", "placeholder" : "Введите ссылку", "size" : 2080}
    ))

class ReportsForm(ModelForm):
    class Meta:
        model = Reports
        fields = ['title', 'short_description','language', 'url']
    
        widgets = {
            'title' : TextInput(
                    attrs = {"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "Название интервью","size" : 80, 'required': True}
            ),
            'short_description' : TextInput(
                attrs = {"type" : "text", "class" : "form-control", "id" : "company", "placeholder" : "Краткое описание","size" : 130, 'required': True}
            ),
            'language' : forms.Select(
                attrs={"class": "form-control", 'required': True,  "id" : "language"},
                choices=LanguageChoice.choices
            )
        }