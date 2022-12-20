from django.db import models
from django.utils.timezone import now
from django.core.validators import validate_image_file_extension
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from PIL import Image
import uuid
import os
import re
from django import forms

# Языки
class LanguageChoice(models.TextChoices):
    RU = "Русский", "Русский"
    KG = "Кыргызча", "Кыргызча"
    EN = "English", "English"
    CH = "中国人", "中国人"
  
# Категория проектов
class ProjectCategory(models.Model):
    Name=models.CharField(max_length=70,verbose_name="Название категории",unique=True,error_messages={'unique':"Категория с таким названием уже существует!"})
    
    class Meta:
        db_table="projectCategory" 
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.Name

#Галерея 
class GalleryProject(models.Model):
    Name=models.CharField(max_length=70,verbose_name="Название галереи", unique=True,error_messages={'unique':"Галерея с таким названием уже существует!"})

    class Meta:
        db_table="galleryProject"
        ordering = ['-id']
        
    def __str__(self) -> str:
        return self.Name


class GalleryNews(models.Model):
    Name=models.CharField(max_length=70,verbose_name="Название галереи", unique=True,error_messages={'unique':"Галерея с таким названием уже существует!"})

    class Meta:
        db_table="galleryNews"
        ordering = ['-id']
    def __str__(self) -> str:
        return self.Name   
    
    
# Функция для кодировки название файла
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_start = filename.replace('.'+ext,'')

    filename = "%s__%s.%s" % (uuid.uuid4(),filename_start, ext)
    return os.path.join(instance.path_url, filename)


# Фото 
class PhotosProject(models.Model):
    URL=models.ImageField(verbose_name="Путь к картинке", upload_to = get_file_path)
    Caption=models.CharField(max_length=110,verbose_name="Название картинки")
    Gallery=models.ForeignKey("galleryProject",on_delete=models.RESTRICT,verbose_name="Галерея")
    
    path_url = "static/client/img/projects/"
    
        
    def __str__(self) -> str:
        return self.Caption 
    
    def save(self, *args, **kwargs):
        super(PhotosProject, self).save(*args, **kwargs)
        image = Image.open(self.URL.path)
        if image.width > 1000 and image.height > 600:
            output_size = (800, 600)
            image.thumbnail(output_size)
            image.save(self.URL.path)
        else:
            raise forms.ValidationError("Размер фотографии не подходит! Минимальный размер 800x600")
    class Meta:
        ordering = ['-id']
    

class PhotosNews(models.Model):
    URL=models.ImageField(verbose_name="Путь картинки", 
                         upload_to = get_file_path,
                         validators = [validate_image_file_extension])
    Caption=models.CharField(max_length=70,verbose_name="Название картинки")
    Gallery=models.ForeignKey("galleryNews",on_delete=models.RESTRICT,verbose_name="Галерея")
    
    path_url = "static/client/img/news/"
  
        
    def __str__(self) -> str:
        return self.Caption 
    
    def save(self, *args, **kwargs):
        super(PhotosNews, self).save(*args, **kwargs)
        image = Image.open(self.URL.path)
        if image.width > 800 and image.height > 400:
            output_size = (600, 400)
            image.thumbnail(output_size)
            image.save(self.URL.path)
        else:
            raise forms.ValidationError("Размер фотографии не подходит! Минимальный размер 800x400")
            
    class Meta:
        ordering = ['-id']
class Contest_Status_Choice(models.TextChoices):
    ON_PROCCESS = "Актуально", "Актуально"
    HAS_FINISHED = "Проведён", "Проведён"
    NOT_FINISHED = "Не Проведён", "Не Проведён"
    
class Project_Status_Choice(models.TextChoices):
    ON_PROCCESS = "В перспективе", "В перспективе"
    HAS_FINISHED = "Реализованные", "Реализованные"

class Vacancy_Status_Choice(models.TextChoices):
    TRUE = "Актуально", "Актуально"
    FALSE = "Данная вакансия не актуальна", "Данная вакансия не актуальна"

# Проекты

class Projects(models.Model):
    Title=models.CharField(max_length=120,verbose_name="Заголовок проекта", unique=True,error_messages={'unique':"Проект с таким названием уже существует!"})
    Short_Description = models.CharField(max_length=200,verbose_name="Краткое описание")
    Description=RichTextField(verbose_name="Описание")
    Date_added=models.DateTimeField(verbose_name="Дата публикации", default=now)
    # Язык проекта
    Language=models.CharField(
                               max_length = 10, 
                               choices = LanguageChoice.choices,
                               default = LanguageChoice.RU,
                               verbose_name = "Язык"
                             )
    Gallery=models.ForeignKey(
        "galleryProject",
        on_delete=models.RESTRICT,
        verbose_name="Галерея"
        )
    Category=models.ForeignKey(
        "projectCategory",
        on_delete=models.RESTRICT,
        verbose_name="Категория"
        )
    Status = models.CharField(
        max_length = 20,
        choices = Project_Status_Choice.choices,
        default = Project_Status_Choice.ON_PROCCESS,
        verbose_name = "Статус"
    )

# Конкурсы

class Contests(models.Model):
    Title=models.CharField(max_length=40,verbose_name="Название конкурса", unique=True,error_messages={'unique':"Конкурс с таким названием уже существует!"})
    Short_Description = models.CharField(max_length=110,verbose_name="Краткое описание")
    Document = models.FileField(
                                verbose_name="Документ", 
                                upload_to=get_file_path, 
                                validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])])
    Date_added=models.DateTimeField(verbose_name="Дата публикации", default=now)
    Language=models.CharField(
                               max_length = 10, 
                               choices = LanguageChoice.choices,
                               default = LanguageChoice.RU,
                               verbose_name = "Язык"
                               )
    Status = models.CharField(
        max_length = 20,
        choices = Contest_Status_Choice.choices,
        default = Contest_Status_Choice.ON_PROCCESS,
        verbose_name = "Статус"
    )
    path_url = "static/client/docs/contest/"
    class Meta:
        ordering = ['-id']
        
    def __str__(self) -> str:
        return self.Caption 

# Новости

class News(models.Model):
    Title=models.CharField(max_length=100,verbose_name="Заголовок новости", unique=True,error_messages={'unique':"Новость с таким названием уже существует!"})
    Short_Description = models.CharField(max_length=200,verbose_name="Краткое описание")
    Description=RichTextField(verbose_name="Описание")
    Date_added=models.DateTimeField(verbose_name="Дата публикации", default=now)
    Language= models.CharField(
                               max_length = 10, 
                               choices = LanguageChoice.choices,
                               default = LanguageChoice.RU,
                               verbose_name = "Язык"
                               )
    Gallery=models.ForeignKey("galleryNews",on_delete=models.RESTRICT,verbose_name="Галерея")
    
    class Meta:
        ordering = ['-id']
    def __str__(self) -> str:
        return self.Title
# Руководство    
class Management(models.Model):
    full_name = models.CharField(max_length = 60, verbose_name = "ФИО Сотрудника")
    position = models.CharField(max_length = 255, verbose_name = "Должность")
    date_birth = models.DateField(verbose_name='Дата рождения', default=now)

    about = RichTextField(verbose_name="Биография сотрудника")

    mail_link = models.CharField(max_length=2080, verbose_name='Ссылка на почту', null=True)
    instagram_link = models.CharField(max_length=2080, verbose_name='Ссылка на инстаграм', null=True)
    facebook_link = models.CharField(max_length=2080, verbose_name='Ссылка на facebook', null=True)

    language=models.CharField(
                               max_length = 10, 
                               choices = LanguageChoice.choices,
                               default = LanguageChoice.RU,
                               verbose_name = "Язык"
                               )
    picture = models.ImageField(
        verbose_name="Фотография", 
        upload_to=get_file_path, 
        validators = [validate_image_file_extension]
        )
    
    path_url = "static/client/img/team/"
    
    def __str__(self):
        return self.full_name

# Вакансии

class Vacancies(models.Model):
    title = models.CharField(max_length=70, verbose_name="Заголовок", unique=True,error_messages={'unique':"Вакансия уже существует!"})
    company = models.CharField(max_length=70, verbose_name = "Компания")
    Language=models.CharField(
                               max_length = 10, 
                               choices = LanguageChoice.choices,
                               default = LanguageChoice.RU,
                               verbose_name = "Язык"
                               )
    pub_date = models.DateTimeField(verbose_name="Дата размещения", default=now)
    positions = models.CharField(max_length = 70, verbose_name="Должность")
    salary = models.CharField(max_length=70, verbose_name="Оклад")
    description = models.TextField(verbose_name = "Описание")
    status = models.CharField(
        max_length = 30,
        choices = Vacancy_Status_Choice.choices,
        default = Vacancy_Status_Choice.TRUE,
        verbose_name = "Статус"
    )
    email_company = models.EmailField(max_length = 40)

# Горячие новости

class HotNewsGallery(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название галереи', unique=True,error_messages={'unique':"Галерея с таким названием уже существует!"})

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['-id']
        
class HotNewsPhoto(models.Model):
    caption = models.CharField(verbose_name='Название фотографии', max_length=70)
    url = models.ImageField(
        verbose_name='Путь картинки',
        upload_to=get_file_path, 
        validators=[validate_image_file_extension]
        )
    gallery = models.ForeignKey(HotNewsGallery, on_delete=models.RESTRICT, verbose_name='Галерея')
    
    
    path_url = "static/client/img/hot_news/"
    
    def __str__(self) -> str:
        return self.caption
    
    def save(self, *args, **kwargs):
        super(HotNewsPhoto, self).save(*args, **kwargs)
        image = Image.open(self.url.path)
        if image.width > 1200 and image.height > 500:
            output_size = (1140, 500)
            image.thumbnail(output_size)
            image.save(self.url.path)
        else:
            raise forms.ValidationError("Размер фотографии не подходит! Минимальный размер 1200x500")
    class Meta: 
        ordering = ['-id']
        
#Главные события
class HotNews(models.Model):
    title = models.CharField(verbose_name='Название событии', max_length=150, unique=True,error_messages={'unique':"Событие с таким названием уже существует!"})
    short_description = models.CharField(verbose_name='Краткое описание', max_length=220)
    description = RichTextField()
    Language=models.CharField(
                               max_length = 10, 
                               choices = LanguageChoice.choices,
                               default = LanguageChoice.RU,
                               verbose_name = "Язык"
                               )
    pub_date = models.DateField(verbose_name="Дата публикации", default=now)
    gallery = models.ForeignKey(HotNewsGallery, on_delete=models.RESTRICT, verbose_name='Галерея')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta: 
        ordering = ['-id']

#Проверка на валидность ссылки
def check_link_validate(link):
        if re.search("^<iframe.*</iframe>$", link):
            return link
        else:
            raise forms.ValidationError('Ссылка не действительна!')

class Interviews(models.Model):
    title = models.CharField(verbose_name='Название ссылки', max_length=80, unique=True,error_messages={'unique':"Такая запись уже существует!"})
    link = models.CharField(verbose_name='Ссылка на статью', max_length=2048, validators=[check_link_validate])


class Reports(models.Model):
    title = models.CharField(verbose_name='Название отчета', max_length=80, unique=True,error_messages={'unique':"Отчет с таким названием уже существует!"})
    short_description = models.CharField(verbose_name='Краткое описание', max_length=130)
    language=models.CharField(
                               max_length = 10, 
                               choices = LanguageChoice.choices,
                               default = LanguageChoice.RU,
                               verbose_name = "Язык",
                               )
    url = models.FileField(
        verbose_name='Путь файла',
        upload_to=get_file_path, 
        validators=[FileExtensionValidator(['pdf','doc', 'docx'])]
        )
    
    path_url = "static/client/docs/reports/"
    
    def __str__(self) -> str:
        return self.caption
    class Meta: 
        ordering = ['-id']
    