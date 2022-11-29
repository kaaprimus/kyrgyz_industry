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
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView



""" 
    Таски:
        Client:
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
            Карта Сайта +
            Горячие событии
            Настроить главную страницу
        Админ:
            Страница авторизации +
            CRUD Операции - Для Новостей +
            CRUD Операции - Для Галерея-Новости +
            CRUD Операции - Для Изображения-Новости +
            
            CRUD Операции - Для Проекта +
            CRUD Операции - Для Галерея-Проект +
            CRUD Операции - Для Изображения-Проект +
            CRUD Операции - Для Категория-Проект +
            
            CRUD Операции - Для Конкурса +
            
            CRUD Операции - Для Галерея - Горячих событии
            CRUD Операции - Для Изображение - Горячих событии 
            CRUD Операции - Для Горячих событии 
            
            Создать - Модель Сотрудники +
            Создать - Модель Вакансии +
            Создать - Модель Горячие событии
            
            Оптимизация Кода
"""


def index(request):
    news= News.objects.order_by('-id')[:4]
    contest= Contests.objects.order_by('-id')[:4]
    hot_news = HotNews.objects.order_by('-id')[:5]
    
    project_ON_PROCCESS=Projects.objects.order_by('-id').filter(Status='В процессе')[:4]
    project_HAS_FINISHED=Projects.objects.order_by('-id').filter(Status='Реализован')[:4]
    project_NOT_FINISHED=Projects.objects.order_by('-id').filter(Status='Не реализован')[:4]
    project_all=Projects.objects.order_by('-id')[:8]
    photo=PhotosProject.objects.all()
    trans = translate(language='ru')
    context = {
        'trans':trans,
        'news_page':news,
        'contest_page':contest,
        'project_ON_PROCCESS':project_ON_PROCCESS,
        'project_HAS_FINISHED':project_HAS_FINISHED,
        'project_NOT_FINISHED':project_NOT_FINISHED,
        'project_all':project_all,
        'photo': photo,
        'hot_news' : hot_news
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
# 703 47 05 64
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

# Карта сайта 
def sitemap(request):
    return render(request, "client/pages/sitemap.html", {})

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

class ProfileView(View):
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('update_profile')
    
    
class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, ProfileView, UpdateView):
    login_url = "login_page"
    success_message = "Данные успешно изменены"
    template_name = 'admin/pages/user/update.html'
    def get_object(self, queryset=None):
        '''This method will load the object
           that will be used to load the form
           that will be edited'''
        return self.request.user
    
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'admin/pages/user/change_password.html'
    success_message = "Пароль успешно изменён"
    success_url = reverse_lazy('update_profile') 

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
    
class NewsCreateView(LoginRequiredMixin, SuccessMessageMixin, NewsView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/news/news-add.html'
    redirect_field_name = "news_create"
    def get(self, request, *args, **kwargs):
        form = NewsForm()
        context = {
            "form" : form,
            "is_active" : "news-panel",
            "active_news" : "active",
            "expand_news" : "show",
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.error(request, "Запись успешно добавлена!")
                return redirect(self.redirect_field_name)
            else:
                messages.error(request, "Введите валидные данные")
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
            "active_news_gallery" : "active",
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
            "active_news_image" : "active",
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
    context = {
         "is_active" : "news-panel",
         "expand_news" : "show",
         "active_news_image" : "active",
    }
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
---- Project-Category Views
""" 
class ProjectCategoryView(View):
    model = ProjectCategory
    form_class = ProjectCategoryForm
    success_url = reverse_lazy("projectcategory_all")
    active_panel = "projects-panel"
    extra_context = {
        "is_active" : active_panel,
        "active_project_category" : "active",
        "expand_projects" : "show",
    }
    
class ProjectCategoryListView(LoginRequiredMixin, ProjectCategoryView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/project-category/category_list.html"
    paginate_by = 10
 
class ProjectCategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, ProjectCategoryView, CreateView):
    login_url = "login_page"
    template_name = "admin/pages/project-category/category_form.html" 
    success_message = "Запись успешно Добавлено!" 
    
class ProjectCategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, ProjectCategoryView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/project-category/category_form.html"
    success_message = "Запись успешно обновлено!" 
    
def projectcategory_delete(request, id):
    context = {
        "is_active" : "projects-panel",
        "active_project_gallery" : "active",
        "expand_projects" : "show",
    }
    obj = get_object_or_404(ProjectCategory, id = id)
    if request.method =="POST":
        try:
        # delete object
            obj.delete()
        # after deleting redirect to
        # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("projectcategory_all")
        except RestrictedError:
            messages.error(request, "Вы не сможете удалить эту категорию, так как это связано с одним или несколькими проектами")
            return redirect("projectcategory_all")
        except Exception as e:
            messages.error(request, e)
            return redirect("projectcategory_all")
    return render(request, "admin/pages/project-category/category_confirm_delete.html", context)

"""
---- End Project-Category Views
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
    paginate_by = 10
    
class ProjectGalleryCreateView(LoginRequiredMixin, SuccessMessageMixin, ProjectGalleryView, CreateView):
    login_url = "login_page"
    template_name = "admin/pages/project-gallery/gallery_form.html"
    redirect_field_name = "projectgallery_create"
    def get(self, request, *args, **kwargs):
        
        form = ProjectGalleryForm()
        context = {
            "form" : form,
            "is_active" : "projects-panel",
            "active_project_gallery" : "active",
            "expand_projects" : "show",
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
    login_url = "login_page"
    template_name = 'admin/pages/project-gallery/gallery_form.html'
    success_message = "Запись успешно обновлено!"      
    

def projectgallery_delete(request, id):
    context = {
        "is_active" : "projects-panel",
        "active_project_gallery" : "active",
        "expand_projects" : "show",
    }
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
---- Project-Image Views
""" 
class ProjectImageView(View):
    login_url = "login_page"
    model = PhotosProject
    form_class = ProjectImageForm
    success_url = reverse_lazy("newsimage_all")
    active_panel = "projects-panel"
    extra_context = {
        "is_active" : active_panel,
        "active_project_image" : "active",
        "expand_projects" : "show",
        }
class ProjectImageListView(LoginRequiredMixin, ProjectImageView, ListView):
    template_name = 'admin/pages/project-image/image_list.html'
    paginate_by = 10
    

class ProjectImageCreateView(LoginRequiredMixin, SuccessMessageMixin,ProjectImageView, CreateView):
    template_name = 'admin/pages/project-image/image_form.html'
    redirect_field_name = "projectimage_create"
    def get(self, request, *args, **kwargs):
        form = ProjectImageForm()
        context = {
            "form" : form,
            "is_active" : self.active_panel,
            "active_project_image" : "active",
            "expand_projects" : "show",
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ProjectImageForm(request.POST, request.FILES)
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

class ProjectImageUpdateView(LoginRequiredMixin, SuccessMessageMixin, ProjectImageView, UpdateView):
    template_name = 'admin/pages/project-image/image_form.html'
    success_message = "Запись успешно обновлено!"
       
    
def projectimage_delete(request, id):
    context = {
        "is_active" : "projects-panel",
        "active_project_image" : "active",
        "expand_projects" : "show",
    }
    obj = get_object_or_404(PhotosProject, id = id)
    if request.method =="POST":
        try:
            if len(obj.URL) > 0:
                os.remove(obj.URL.path)
            obj.delete()
            
            messages.success(request, "Запись успешно удалено!")
            return redirect("projectimage_all")
        except Exception as e:
            messages.error(request, e)
            return redirect("projectimage_delete")
    return render(request, "admin/pages/project-image/image_confirm_delete.html", context)

"""
---- End Project-Image Views
""" 

"""
---- Project Views
""" 
class ProjectView(View):
    model = Projects
    form_class = ProjectForm
    active_panel = "projects-panel"
    extra_context = {
        "is_active" : active_panel,
        "active_projects" : "active",
        "expand_projects" : "show",
        }
    
class ProjectListView(LoginRequiredMixin, ProjectView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/project/project_list.html"
    

class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, ProjectView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/project/project_form.html'
    redirect_field_name = "projects_create"
    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        context = {
            "form" : form,
            "is_active" : self.active_panel,
            "active_projects" : "active",
            "expand_projects" : "show",
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            try:
                form.save()
                messages.success(request, "Запись успешно добавлено!")
                return redirect(self.redirect_field_name)
            except Exception as e:
                messages.error(request, e)
                return redirect(self.redirect_field_name)
        else:
            messages.error(request, "Invalid Method"        )
            return redirect(self.redirect_field_name)     
        
class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, ProjectView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/project/project_form.html"
    
    
def projects_delete(request, id):
    context = {
            "is_active" : "projects-panel",
            "active_projects" : "active",
            "expand_projects" : "show",
    }
    obj = get_object_or_404(Projects, id = id)
    if request.method =="POST":
        
        try:
            # delete object
            obj.delete()
            # after deleting redirect to
            # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("projects_all")
        except Exception as e:
            messages.error(request, "Не удалось удалить запись, повторите попытку!")
            return redirect("projects_all")
 
    return render(request, "admin/pages/projects/project_confirm_delete.html", context)      
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
            "active_contests" : "active",
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


class ManagementView(View):
    model = Management
    form_class = ManagementForm
    active_panel = 'management-panel'
    extra_context = {
        "is_active" : active_panel,
        "active_management" : "active",
        "expand_management" : "show",
        }
    
class ManagementListView(LoginRequiredMixin, ManagementView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/management/management_list.html"

class ManagementCreateView(LoginRequiredMixin, SuccessMessageMixin, ManagementView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/management/management_form.html'
    success_url = reverse_lazy("management_create")
    success_message = "Запись успешно добавлена!"
   
        
        
class ManagementUpdateView(LoginRequiredMixin, SuccessMessageMixin, ManagementView, UpdateView):
    login_url = 'login_page'
    success_url = reverse_lazy("management_all")
    template_name = 'admin/pages/management/management_form.html'
    success_message = "Запись успешно обновлена!"
    
    
def management_delete(request, id):
    context = {
         "is_active" : "management-panel",
         "active_management" : "active",
         "expand_management" : "show",
    }
    obj = get_object_or_404(Management, id = id)
    if request.method =="POST":
        
        try:
            # delete object
            obj.delete()
            # after deleting redirect to
            # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("management_all")
        except Exception as e:
            messages.error(request, "Не удалось удалить запись, повторите попытку!")
            return redirect("management_all")
 
    return render(request, "admin/pages/management/management_confirm_delete.html", context)      

    
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

"""
---- End Vacancies Views
"""  

"""
---- HotNews-Gallery Views
"""  
class HotNewsGalleryView(View):
    model = HotNewsGallery
    form_class = HotNewsGalleryForm
    success_url = reverse_lazy("hotnewsgallery_all")
    extra_context = {
        "is_active" : "hotnews-panel",
        "active_hotnews_gallery" : "active",
        "expand_hotnews" : "show",
        }
    
class HotNewsGalleryListView(LoginRequiredMixin, HotNewsGalleryView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/hotnews-gallery/gallery_list.html"
    paginate_by = 10
    
class HotNewsGalleryCreateView(LoginRequiredMixin, SuccessMessageMixin, HotNewsGalleryView, CreateView):
    login_url = "login_page"
    template_name = "admin/pages/hotnews-gallery/gallery_form.html"
    redirect_field_name = "hotnewsgallery_create"
    success_message = "Запись успешно Добавлена!"
class HotNewsGalleryUpdateView(LoginRequiredMixin, SuccessMessageMixin, HotNewsGalleryView, UpdateView):
    login_url = "login_page"
    template_name = 'admin/pages/hotnews-gallery/gallery_form.html'
    success_message = "Запись успешно обновлено!"      
    

def hotnewsgallery_delete(request, id):
    context = {
        "is_active" : "hotnews-panel",
        "active_hotnews_gallery" : "active",
        "expand_hotnews" : "show",
    }
    obj = get_object_or_404(HotNewsGallery, id = id)
    if request.method =="POST":
        try:
        # delete object
            obj.delete()
        # after deleting redirect to
        # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("hotnewsgallery_all")
        except RestrictedError:
            messages.error(request, "Вы не сможете удалить эту галерею, так как это связано с одной или несколькими новостями или фотографиями")
            return redirect("hotnewsgallery_all")
    return render(request, "admin/pages/hotnews-gallery/gallery_confirm_delete.html", context)

"""
---- End HotNews-Gallery Views
"""    

"""
---- HotNews-Image Views
""" 
class HotNewsImageView(View):
    login_url = "login_page"
    model = HotNewsPhoto
    form_class = HotNewsImageForm
    success_url = reverse_lazy("hotnewsimage_all")
    active_panel = "hotnews-panel"
    extra_context = {
        "is_active" : active_panel,
        "active_hotnews_image" : "active",
        "expand_hotnews" : "show",
        }
class HotNewsImageListView(LoginRequiredMixin, HotNewsImageView, ListView):
    template_name = 'admin/pages/hotnews-image/image_list.html'
    paginate_by = 10
    

class HotNewsImageCreateView(LoginRequiredMixin, SuccessMessageMixin,HotNewsImageView, CreateView):
    template_name = 'admin/pages/hotnews-image/image_form.html'
    redirect_field_name = "hotnewsimage_create"
    def get(self, request, *args, **kwargs):
        form = HotNewsImageForm()
        context = {
            "form" : form,
            "is_active" : self.active_panel,
            "active_hotnews_image" : "active",
            "expand_hotnews" : "show",
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = HotNewsImageForm(request.POST, request.FILES)
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

class HotNewsImageUpdateView(LoginRequiredMixin, SuccessMessageMixin, HotNewsImageView, UpdateView):
    template_name = 'admin/pages/hotnews-image/image_form.html'
    success_message = "Запись успешно обновлено!"
       
    
def hotnewsimage_delete(request, id):
    context = {
        "is_active" : "projects-panel",
        "active_project_image" : "active",
        "expand_projects" : "show",
    }
    obj = get_object_or_404(PhotosProject, id = id)
    if request.method =="POST":
        try:
            if len(obj.url) > 0:
                os.remove(obj.url.path)
            obj.delete()
            
            messages.success(request, "Запись успешно удалена!")
            return redirect("hotnewsimage_all")
        except Exception as e:
            messages.error(request, e)
            return redirect("hotnewsimage_delete")
    return render(request, "admin/pages/hotnews-image/image_confirm_delete.html", context)

"""
---- End HotNews-Image Views
""" 

"""
---- HotNews Views
""" 
class HotNewsView(View):
    model = HotNews
    form_class = HotNewsForm
    active_panel = "hotnews-panel"
    extra_context = {
        "is_active" : active_panel,
        "active_hotnews" : "active",
        "expand_hotnews" : "show",
        }
    
class HotNewsListView(LoginRequiredMixin, HotNewsView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/hotnews/hotnews_list.html"
    paginate_by = 10

class HotNewsCreateView(LoginRequiredMixin, SuccessMessageMixin, HotNewsView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/hotnews/hotnews_form.html'
    success_message = "Запись успешно Добавлена!"  

class HotNewsUpdateView(LoginRequiredMixin, SuccessMessageMixin, HotNewsView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/hotnews/hotnews_form.html"
    success_message = "Запись успешно Обновлена!"  
    
def hotnews_delete(request, id):
    context = {
            "is_active" : "hotnews-panel",
            "active_hotnews" : "active",
            "expand_hotnews" : "show",
    }
    obj = get_object_or_404(HotNews, id = id)
    if request.method =="POST":
        
        try:
            # delete object
            obj.delete()
            # after deleting redirect to
            # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("hotnews_all")
        except Exception as e:
            messages.error(request, "Не удалось удалить запись, повторите попытку!")
            return redirect("hotnews_delete")
 
    return render(request, "admin/pages/hotnews/hotnews_confirm_delete.html", context)   

