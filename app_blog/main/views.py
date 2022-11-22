import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.shortcuts import get_object_or_404
from django.db.models.deletion import RestrictedError
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.backends import UserModel
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.conf import settings
from django.core.paginator import Paginator


""" 

    Таски:
        Клиент:
            Вывод Новостей+
            Архив новостей
            Вывод Проекта
            Вывод Конкурса
            Вывод Вакансии
            Вывод Структуры
            Страницы для Детально
            Создать страницу для Галереи
            Создать карту сайта
            Обратная связь+
            Страница для вакансии и вывод активных вакансии
            
        Админ:
            Страница авторизации
            CRUD Операции - Для Новостей
            CRUD Операции - Для Галерея-Новости
            CRUD Операции - Для Изображения-Новости
            
            CRUD Операции - Для Проекта
            CRUD Операции - Для Галерея-Проект
            CRUD Операции - Для Изображения-Новости
            
            CRUD Операции - Для Конкурса
            CRUD Операции - Для Галерея-Конкурс
            CRUD Операции - Для Изображения-Конкурс
            
            Создать - Модель Сотрудники
            Создать - Модель Вакансии

"""

def index(request):
    news= News.objects.order_by('-id')[:4]
    contest= Contests.objects.order_by('-id')[:4]
    
    project_ON_PROCCESS=Projects.objects.order_by('-id').filter(Status='В процессе')[:4]
    project_HAS_FINISHED=Projects.objects.order_by('-id').filter(Status='Реализован')[:4]
    project_NOT_FINISHED=Projects.objects.order_by('-id').filter(Status='Не реализован')[:4]
    project_all=Projects.objects.order_by('-id')[:8]
    photo=PhotosProject.objects.all()
    trans = translate(language='ru')
    context = {'trans':trans,'news_page':news,'contest_page':contest,
        'project_ON_PROCCESS':project_ON_PROCCESS,'project_HAS_FINISHED':project_HAS_FINISHED,
        'project_NOT_FINISHED':project_NOT_FINISHED,'project_all':project_all,'photo': photo
        }
    return render(request, "client/index.html", context)

def about_company(request):
    trans = translate(language='ru')
    context = {'trans':trans}
    return render(request, "client/pages/about_company.html", context)

def blog_detail(request):
    trans = translate(language='ru')
    context = {'trans':trans}
    return render(request, "client/pages/blog_detail.html", context)

def president(request):
    trans = translate(language='ru')
    context = {'trans':trans}
    return render(request, "client/pages/president.html", context)

def inner_page(request):
    trans = translate(language='ru')
    context = {'trans':trans}
    return render(request, "client/pages/inner-page.html", context)

def gallery(request):
    trans = translate(language='ru')
    context = {'trans':trans}
    return render(request, "client/pages/gallery.html", context)

def contests(request,number_page=1):
    trans = translate(language='ru')
    contest= Contests.objects.order_by('-id')
    currunt_page_news = Paginator(contest,2)
    context = {'contest_page': currunt_page_news.page(number_page),'trans':trans}
    return render(request, "client/pages/contests.html", context)

def news(request,number_page=1):
    news= News.objects.order_by('-id')
    photo=PhotosNews.objects.all()
    currunt_page_news = Paginator(news,4)
    trans = translate(language='ru')
    context = {'news_page': currunt_page_news.page(number_page),'trans':trans, 'photo':photo}
    return render(request, "client/pages/news.html", context)


def projects(request,number_page=1):
    project= Projects.objects.order_by('-id')
    currunt_page_news = Paginator(project,2)
    photo=PhotosProject.objects.all()
    trans = translate(language='ru')
    context = {'project_page':currunt_page_news.page(number_page),'photo':photo,'trans':trans}
    return render(request, "client/pages/projects.html", context)

def get_news(request,title):
    trans = translate(language='ru')
    news_detail=News.objects.filter(Title=title)
    news_title=News.objects.get(Title=title)
    photo=PhotosNews.objects.filter(Gallery_id=get_id_Gallery_News(title))
    context = {'news_detail': news_detail,'photo':photo,'news_title':news_title,'trans':trans}
    return render(request, "client/pages/news_detail.html", context)

def get_project(request,title):
    trans = translate(language='ru')
    project_detail=Projects.objects.filter(Title=title)
    project_title=Projects.objects.get(Title=title)
    photo=PhotosProject.objects.filter(Gallery_id=get_id_Gallery_project(title))
    context = {'project_detail': project_detail,'photo':photo,'project_title':project_title,'trans':trans}
    return render(request, "client/pages/project_detail.html", context)

def get_id_Gallery_News(title):
    news_detail=News.objects.filter(Title=title)
    id=0
    for val in news_detail:
        id=val.Gallery_id
    return id

def get_id_Gallery_project(title):
    project_detail=Projects.objects.filter(Title=title)
    id=0
    for val in project_detail:
        id=val.Gallery_id
    return id


def project_detail(request):
    trans = translate(language='ru')
    context = {'trans':trans}
    return render(request, "client/pages/project_detail.html", context)

def veep(request):
    trans = translate(language='ru')
    context = {'trans':trans}
    return render(request, "client/pages/veep.html", context)

def npa(request):
    trans = translate(language='ru')
    context = {'trans':trans}
    return render(request, "client/pages/NPA.html", context)

def vacancies(request, number_page=1):
    trans = translate(language='ru')
    contest= Vacancies.objects.order_by('-id')
    currunt_page_vacancies = Paginator(contest,4)
    context = {'currunt_page_vacancies': currunt_page_vacancies.page(number_page),'trans':trans}
    return render(request, "client/pages/vacancies.html", context)

def get_vacancy(request,title):
    trans = translate(language='ru')
    vacancy_detail=Vacancies.objects.filter(title=title)
    vacancy_title=Vacancies.objects.get(title=title)
    context = {'vacancy_detail': vacancy_detail,'vacancy_title':vacancy_title,'trans':trans}
    return render(request, "client/pages/vacancy_detail.html", context)

def gallery_page(request,number_page=1):
    trans = translate(language='ru')
    news_photo=PhotosNews.objects.order_by('-id')
    projects_photo=PhotosProject.objects.order_by('-id')
    gallery_page = Paginator(news_photo,4)
    context = {'gallery_page': gallery_page.page(number_page),'trans':trans, 'news_photo':news_photo}
    return render(request, "client/pages/gallery.html", context)

def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('hello')
    finally:
        activate(cur_language)
    return text

def error_404(request, exception):
   context = {}
   return render(request,'admin/404.html', context)

def error_500(request):
   context = {}
   return render(request,'admin/500.html', context)

def error_503(request):
   context = {}
   return render(request,'admin/503.html', context)


def send_message(request):
    
    sucs=True
    if request.method == 'POST':
        settings.EMAIL_HOST_USER=request.POST.get('email', '')
        settings.EMAIL_HOST_PASSWORD=''
        Name = request.POST.get('name', '')
        
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')
        subject = "Сообщение от пользователей" 
        try:
            
            body = {
			    'Name: ': "От кого: "+ Name, 
                'from_email': "Эл.адрес: " + from_email,
			    'message': "Сообщение: " + message,
		    }
	    
            messageAll = "\n".join(body.values())
            send_mail(subject, messageAll, from_email, ['To'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except:
            messages.add_message(request, messages.ERROR, 'Неправильный эл.адрес')
            sucs=False
    if(sucs==True):
        messages.add_message(request, messages.SUCCESS, 'Ваше сообщение отправлено!')
    return redirect ('/')



def detail(request):
    template_name = "client/pages/blog_detail.html"
    return render(request, template_name, {})

@csrf_exempt
def login_page(request):
    success_url = reverse_lazy('admin_panel')
    template_name = "admin/pages/forms/login.html"
    if request.user.is_authenticated:
        return redirect(success_url)
    else:
        return render(request, template_name, {})


@csrf_exempt
def authorization(request):
    success_url = reverse_lazy('admin_panel')
    username = request.POST['username']
    password = request.POST['password']
    
    try:
        account = authenticate(username=UserModel.objects.get(email=username).username, password=password)
        if account is not None and request.method == 'POST':
            login(request, account)
            return redirect(success_url)
        else:
            messages.error(request, "Логин или пароль неправильно")
            return redirect('login_page')
    except:
        if username == "":
            messages.error(request, "Введите ваш Логин или E-mail")
            return redirect('login_page')
        elif password == "":
            messages.error(request, "Введите пароль")
            return redirect('login_page')
        else:
            account = authenticate(username=username, password=password)
            if account is not None and request.method == 'POST':
                login(request, account)
                return redirect(success_url)
            else:
                messages.error(request, "Логин или пароль неправильно")
                return redirect('login_page')
   

def logout_page(request):
    logout(request)
    return redirect('login_page')

# Admin-Panel Views
@login_required
def admin_index_page(request):
    template_name = "admin/admin.html"
    context = {
        "is_active" : "main-panel"
    }
    return render(request, template_name, context)

@login_required
def admin_form_page(request):
    template_name = "admin/pages/forms/basic_elements.html"

    user_name = None
    if request.user.is_authenticated:
        user_name = request.user.username
    context = {
        "user" : user_name
    }
    return render(request, template_name, context)




class NewsView(View):
    model = News
    form_class = NewsForm
    success_url = reverse_lazy('news_all')
    extra_context = {
        "is_active" : "news-panel",
        "active_news" : "active",
        "expand_news" : "show",
        }

class NewsListView(LoginRequiredMixin, NewsView, ListView):
    login_url = 'login_page'
    template_name = 'admin/pages/news/news-all.html'
    paginate_by = 10
    
class NewsCreateView(LoginRequiredMixin, NewsView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/news/news-add.html'
    redirect_field_name = "news_create"
    def get(self, request, *args, **kwargs):
        
        form = NewsForm()
        context = {
            "form" : form,
            "is_active" : "news-panel",
            "expand_news" : "show",
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.redirect_field_name)
            else:
                return redirect(self.redirect_field_name)
        else:
            messages.error(request, "Invalid Method")
            return redirect(self.redirect_field_name) 


    
class NewsUpdateView(LoginRequiredMixin,SuccessMessageMixin, NewsView, UpdateView):
    login_url = 'login_page'
    success_url = reverse_lazy("news_all")
    template_name = "admin/pages/news/news-edit.html"
    success_message = "Запись успешно обновлена!"
        
           
def news_delete(request, id):
    context = {}
    obj = get_object_or_404(News, id = id)
    if request.method =="POST":
        
        try:
            # delete object
            obj.delete()
            # after deleting redirect to
            # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("news_all")
        except Exception as e:
            messages.error(request, "Не удалось удалить запись, повторите попытку!")
            return redirect("news_all")
 
    return render(request, "admin/pages/news/news_delete.html", context)

class NewsDetailView(LoginRequiredMixin, SuccessMessageMixin, NewsView, DetailView):
    login_url = "login_page"
    template_name = "admin/pages/news/news-detail.html"
"""
---- News-Gallery Views
"""
class NewsGalleryView(View):
    model = GalleryNews
    form_class = NewsGalleryForm
    extra_context = {
        "is_active" : "news-panel",
        "active_news_gallery" : "active",
        "expand_news" : "show",
        }

class NewsGalleryListView(LoginRequiredMixin, NewsGalleryView, ListView):
    login_url = 'login_page'
    template_name = 'admin/pages/news-gallery/newsgallery_list.html'
    paginate_by = 10

class NewsGalleryCreateView(LoginRequiredMixin, NewsGalleryView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/news-gallery/newsgallery_form.html'
    redirect_field_name = "newsgallery_create"
    def get(self, request, *args, **kwargs):
        form = NewsGalleryForm()
        context = {
            "form" : form,
            "is_active" : "news-panel",
            "expand_news" : "show",
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = NewsGalleryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Запись Успешно добавлено!")
                return redirect(self.redirect_field_name)
            else:
                messages.error(request, "Введите корректные данные!!")
                return redirect(self.redirect_field_name)
        else:
            messages.error(request, "Invalid Method")
            return redirect(self.redirect_field_name) 

class NewsGalleryUpdateView(LoginRequiredMixin, SuccessMessageMixin, NewsGalleryView, UpdateView):
    template_name = 'admin/pages/news-gallery/newsgallery_form.html'
    success_url = reverse_lazy("newsgallery_all")
    success_message = "Запись успешно обновлено!"      
    
def newsgallery_delete(request, id):
    context = {}
    obj = get_object_or_404(GalleryNews, id = id)
    if request.method =="POST":
        try:
        # delete object
            obj.delete()
        # after deleting redirect to
        # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("newsgallery_all")
        except RestrictedError:
            messages.error(request, "Вы не сможете удалить эту галерею, так как это связано с одной или несколькими новостями или фотографиями")
            return redirect("newsgallery_all")
    return render(request, "admin/pages/news-gallery/newsgallery_confirm_delete.html", context)

"""
---- End News-Gallery Views
"""
"""
---- News-Image Views
"""
class NewsImageView(View):
    model = PhotosNews
    form_class = NewsImageForm
    success_url = reverse_lazy("newsimage_all")
    login_url = "login_page"
    extra_context = {
        "is_active" : "news-panel",
        "active_news_image" : "active",
        "expand_news" : "show",
        }
class NewsImageListView(LoginRequiredMixin, NewsImageView, ListView):
    template_name = 'admin/pages/news-image/newsimage_list.html'
    paginate_by = 10
    

class NewsImageCreateView(LoginRequiredMixin, NewsImageView, CreateView):
    template_name = 'admin/pages/news-image/newsimage_form.html'
    redirect_field_name = "newsimage_create"
    def get(self, request, *args, **kwargs):
        form = NewsImageForm()
        context = {
            "form" : form,
            "is_active" : "news-panel",
            "expand_news" : "show",
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = NewsImageForm(request.POST, request.FILES)
            try:
                form.save()
                messages.success(request, "Изображение Успешно добавлено!")
                return redirect(self.redirect_field_name)
            except ValueError:
                messages.error(request, "Выберите картинку в формате (jpg, jpeg, png, и т.д.)")
                return redirect(self.redirect_field_name)
            except Exception as e:
                messages.error(request, e)
                return redirect(self.redirect_field_name)
        else:
            messages.error(request, "Invalid Method")
            return redirect(self.redirect_field_name) 

class NewsImageUpdateView(LoginRequiredMixin, NewsImageView, UpdateView):
    template_name = 'admin/pages/news-image/newsimage_form.html'
    success_message = "Запись успешно обновлено!"
       
    
class NewsImageDeleteView(LoginRequiredMixin, NewsGalleryView, DeleteView):
    template_name = 'admin/pages/news-gallery/newsgallery_confirm_delete.html'
    success_message = "Запись успешно удалено!"
    
def newsimage_delete(request, id):
    context = {}
    obj = get_object_or_404(PhotosNews, id = id)
    if request.method =="POST":
        try:
            if len(obj.URL) > 0:
                os.remove(obj.URL.path)
            obj.delete()
            
            messages.success(request, "Запись успешно удалено!")
            return redirect("newsimage_all")
        except Exception as e:
            messages.error(request, e)
            return redirect("newsimage_delete")
    return render(request, "admin/pages/news-image/newsimage_confirm_delete.html", context)
"""
---- End News-Image Views
"""    


"""
---- Project-Gallery Views
"""  
class ProjectGalleryView(View):
    model = GalleryProject
    form_class = ProjectGalleryForm
    success_url = reverse_lazy("projectgallery_all")
    extra_context = {
        "is_active" : "projects-panel",
        "active_project_gallery" : "active",
        "expand_projects" : "show",
        }
    
class ProjectGalleryListView(LoginRequiredMixin, ProjectGalleryView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/project-gallery/gallery_list.html"

class ProjectGalleryCreateView(LoginRequiredMixin, SuccessMessageMixin, ProjectGalleryView, CreateView):
    login_url = "login_page"
    template_name = "admin/pages/project-gallery/gallery_create.html"
    redirect_field_name = "newsgallery_create"
    def get(self, request, *args, **kwargs):
        
        form = ProjectGalleryForm()
        context = {
            "form" : form,
            "is_active" : "gallery-panel",
            "expand_gallery" : "show",
            "active_create_gallerynews" : "active"
            
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ProjectGalleryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Запись Успешно добавлено!")
                return redirect(self.redirect_field_name)
            else:
                messages.error(request, "Введите валидные данные!")
                return redirect(self.redirect_field_name)
        else:
            messages.error(request, "Invalid Method")
            return redirect(self.redirect_field_name) 
        

class ProjectGalleryUpdateView(LoginRequiredMixin, SuccessMessageMixin, ProjectGalleryView, UpdateView):
    template_name = 'admin/pages/project-gallery/gallery_form.html'
    success_message = "Запись успешно обновлено!"      
    

def projectgallery_delete(request, id):
    context = {}
    obj = get_object_or_404(GalleryProject, id = id)
    if request.method =="POST":
        try:
        # delete object
            obj.delete()
        # after deleting redirect to
        # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("newsgallery_all")
        except RestrictedError:
            messages.error(request, "Вы не сможете удалить эту галерею, так как это связано с одной или несколькими проектами или фотографиями")
            return redirect("newsgallery_all")
    return render(request, "admin/pages/news-gallery/newsgallery_confirm_delete.html", context)
"""
---- End Project-Gallery Views
"""    



"""
---- Contest Views
"""  
class ContestView(View):
    model = Contests
    form_class = ContestForm
    success_url = reverse_lazy("contests_all")
    extra_context = {
        "is_active" : "contests-panel",
        "active_contests" : "active",
        "expand_contests" : "show",
        }
    

class ContestListView(LoginRequiredMixin, ContestView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/contests/contests_list.html"
    

class ContestCreateView(LoginRequiredMixin, SuccessMessageMixin, ContestView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/contests/contests_form.html"
    redirect_field_name = "contests_create"
    def get(self, request, *args, **kwargs):
        
        form = ContestForm()
        context = {
            "form" : form,
            "is_active" : "contests-panel",
            "expand_contests" : "show",
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ContestForm(request.POST, request.FILES)
            try:
                form.save()
                messages.success(request, "Успешно добавлено!")
                return redirect(self.redirect_field_name)
            except ValueError:
                messages.error(request, "Выберите файлы в формате (.pdf, .docx, .doc)")
                return redirect(self.redirect_field_name)
            except Exception as e:
                messages.error(request, e)
                return redirect(self.redirect_field_name)
        else:
            messages.error(request, "Invalid Method")
            return redirect(self.redirect_field_name) 
        
class ContestUpdateView(LoginRequiredMixin, SuccessMessageMixin, ContestView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/contests/contests_form.html"

def contests_delete(request, id):
    context = {}
    obj = get_object_or_404(Contests, id = id)
    if request.method =="POST":
        try:
            if len(obj.Document) > 0:
                os.remove(obj.Document.path)
            obj.delete()
            
            messages.success(request, "Запись успешно удалено!")
            return redirect("contests_all")
        except Exception as e:
            messages.error(request, e)
            return redirect("contests_delete")
    return render(request, "admin/pages/contests/contests_confirm_delete.html", context)



def get_last_projects(request):
    last_ten = Projects.objects.all().order_by('-id')[:10]
    template_name = "admin/admin.html"
    context = {
        "last_projects" : last_ten
    }
    
    return render(request, template_name, context)

class VacanciesView(View):
    model = Vacancies
    form_class = VacanciesForm
    active_panel = "vacancies-panel"
    extra_context = {
        "is_active" : active_panel,
        "active_vacancies" : "active",
        "expand_vacancies" : "show",
        }
    
class VacanciesListView(LoginRequiredMixin, VacanciesView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/vacancies/vacancies_list.html"
    

class VacanciesCreateView(LoginRequiredMixin, SuccessMessageMixin, VacanciesView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/vacancies/vacancies_form.html'
    redirect_field_name = "vacancies_create"
    def get(self, request, *args, **kwargs):
        form = VacanciesForm()
        context = {
            "form" : form,
            "is_active" : self.active_panel,
            "active_vacancies" : "active",
            "expand_vacancies" : "show",
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = VacanciesForm(request.POST)
            try:
                form.save()
                messages.success(request, "Запись успешно добавлено!")
                return redirect(self.redirect_field_name)
            except Exception as e:
                messages.error(request, e)
                return redirect(self.redirect_field_name)
        else:
            messages.error(request, "Invalid Method")
            return redirect(self.redirect_field_name)     
        
class VacanciesUpdateView(LoginRequiredMixin, SuccessMessageMixin, VacanciesView, UpdateView):
    login_url = 'login_page'
    success_url = reverse_lazy("vacancies_all")
    template_name = 'admin/pages/vacancies/vacancies_edit.html'
    success_message = "Запись успешно обновлена!"
    
    
def vacancies_delete(request, id):
    context = {}
    obj = get_object_or_404(Vacancies, id = id)
    if request.method =="POST":
        
        try:
            # delete object
            obj.delete()
            # after deleting redirect to
            # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("vacancies_all")
        except Exception as e:
            messages.error(request, "Не удалось удалить запись, повторите попытку!")
            return redirect("vacancies_all")
 
    return render(request, "admin/pages/vacancies/vacancies_confirm_delete.html", context)      
