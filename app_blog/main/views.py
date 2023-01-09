import os
import smtplib
from validate_email import validate_email
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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
""" 
    Таски:
        Client:
            Вывод Новостей  +
            Архив новостей  +
            Вывод Проекта   +
            Вывод Конкурса  +
            Вывод Вакансии  +
            Вывод Структуры
            Страницы для Детально   
            Создать страницу для Галереи    +
            Создать карту сайта
            Обратная связь  +
            Страница для вакансии и вывод активных вакансии +
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

def password_reset_request(request):
    settings.EMAIL_HOST_USER='kyrgyzindustry.portal.01@gmail.com'
    settings.EMAIL_HOST_PASSWORD='jenpktauntyqbeum'
    if request.method == "POST":
        
        password_reset_form = UserPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Запрос на сброс данных"
                    email_template_name = "admin/pages/user/password_reset_email.html"
                    c = {
                        "email":user.email,
                        'domain':'http://127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    email = render_to_string(email_template_name, c)
                    
                    try:
                        send_mail(subject, email, 'zenisbekovk04@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        
                        return HttpResponse('Invalid header found.')
                    
                    return redirect ("/accounts/password_reset/done/")
    password_reset_form = UserPasswordResetForm()
    return render(request=request, template_name="admin/pages/user/password_reset.html", context={"password_reset_form":password_reset_form})

# Функция для тестировки
def test_method(request):
    news= News.objects.order_by('-id')[:2]
    print(news)
    arr = []
    for s in news:
        img = PhotosNews.objects.filter(Gallery = s.Gallery).first()
        arr.append(img.URL)
    mix = zip(news, arr)
    print(arr)
    context = {
        "news" : mix,
    }
    
    return render(request, 'client/pages/img.html', context)
    
# Блоки
def get_block_detail(request,titleblock):
    trans = translate(language='ru')
    blockslen = Blocks.objects.filter(language = get_lang(trans=trans),title=titleblock)
    context = {'trans':trans, 'blocks':blockslen}
    return render(request, "client/pages/blockone.html", context)

# Получаем выбранный язык для фильтрации
def get_lang(trans):
    if trans == 'en':
        lang = 'English'
    elif trans == 'zh-hans':
        lang = '中国人'
    elif trans == 'ky':
        lang = 'Кыргызча'
    else:
        lang = 'Русский'
    return lang

def index(request):
    trans = translate(language='ru')
    
    news = News.objects.filter(Language = get_lang(trans=trans)).order_by('-Date_added')[:4]
    hot_news = HotNews.objects.filter(Language = get_lang(trans=trans)).order_by('-pub_date')[:5]
    
    error = False
    # Получаем первую фотографию под новостями
    first_image = []
    for post in news:
        img = PhotosNews.objects.filter(Gallery = post.Gallery).first()
        if img is None:
            error = True
        else:
            first_image.append(img.URL)
            
    hotnews_error = False     
    hot_news_img = []
    for post in hot_news:
        img = HotNewsPhoto.objects.filter(gallery = post.gallery).first()
        print(img)
        if img is None:
            error = True
        else:
            hot_news_img.append(img.url)
            
    news_image_mixed = zip(news, first_image)   
    hot_news_mixed = zip(hot_news, hot_news_img)   
 
    context = {
        'trans':trans,
        'news_page':news_image_mixed,
        'hot_news' : hot_news_mixed,
        "error" : error
        }
    return render(request, "client/index.html", context)

    

def interviews(request):
    trans = translate(language='ru')
    posts = Interviews.objects.order_by('-id')

    per_page = 6
    
    actual_url = request.path.split('/')[2]

    currunt_page_interview = Paginator(posts, per_page=per_page)
    
    page_num = currunt_page_interview.num_pages
    try:
        page = request.GET.get("page", 1)
        posts = currunt_page_interview.page(page)

    except (PageNotAnInteger, TypeError):
        posts = currunt_page_interview.page(1)
        
    except EmptyPage:
        posts = currunt_page_interview.page(currunt_page_interview.num_pages)  

    context = {
        'posts':posts,
        'paginator': currunt_page_interview,
        'all_interviews':posts,
        'trans':trans,
        'page_num':page_num,
        'actual_url':actual_url
        }
    return render(request, "client/pages/interviews.html", context)


def get_president_position(language):
    if language == "en":
        position = "President"
    elif language == "zh-hans":
        position = "总统"
    else:
        position = "Президент"
        
    return position

def get_translated_position(language):
    if language == "en":
        position = "Vice-President"
    elif language == "zh-hans":
        position = "副总统"
    else:
        position = "Вице-президент"
        
    return position

def get_advisor(language):
    if language == "en":
        position = "Advisor"
    elif language == "zh-hans":
        position = "顾问"
    elif language == "ru":
        position = "Советник"
    else:
        position = "Кеңешчи"

    return position

def about_company(request):
    trans = translate(language='ru')
    blocks = Blocks.objects.all().filter(language = get_lang(trans=trans))     
    actual_url = request.path.split('/')[2]
    
    president = None
    not_exist = False
    try:
        president = Management.objects.get(position__startswith=get_president_position(language=trans))  
    except Management.DoesNotExist:
        not_exist = True
    try:
        veep = Management.objects.filter(position__startswith=get_translated_position(language=trans)).order_by('id')[:4]
    except Management.DoesNotExist:
        not_exist = True
    try:
        advisor = Management.objects.filter(position__startswith=get_advisor(language=trans)).order_by('id')[:4]
    except Management.DoesNotExist:
        not_exist = True
    
    context = {
        'trans':trans, 
        'veep':veep,
        "not_exist" : not_exist,
        'president':president,
        'actual_url':actual_url,
        'advisor':advisor,
        'blocks':blocks
        }
    return render(request, "client/pages/about_company.html", context)

def about_us_full_info(request):
    actual_url = request.path.split('/')[2]

    trans = translate(language='ru')
    context = {
        'trans':trans,
        'actual_url':actual_url
    }
    return render(request, "client/pages/about_us_full_info.html", context)

def president(request):
    trans = translate(language='ru')

    not_exist = False
    try:
        president = Management.objects.get(position__startswith=get_president_position(language=trans))
    except Management.DoesNotExist:
        not_exist = True
        
    context = {
        'trans':trans,
        'president':president,
        "not_exist" : not_exist
        }

    return render(request, "client/pages/president.html", context)

def advisor(request):
    trans = translate(language='ru')

    not_exist = False
    try:
        advisor = Management.objects.get(position__startswith=get_advisor(language=trans))
    except Management.DoesNotExist:
        not_exist = True
        
    context = {
        'trans':trans,
        'president':advisor,
        "not_exist" : not_exist
        }

    return render(request, "client/pages/advisors.html", context)


def contests(request):
    per_page = 6
    actual_url = request.path.split('/')[2]

    trans = translate(language='ru')
    contest= Contests.objects.all().filter(Language = get_lang(trans=trans)).order_by('-Date_added')
    paginator = Paginator(contest, per_page=per_page)    
    
    pag_num = paginator.num_pages
    try:
        page = request.GET.get("page", 1)   
        contest = paginator.page(page) 
    except (PageNotAnInteger, TypeError):
        contest = paginator.page(1)
    except EmptyPage:
        contest = paginator.page(pag_num)
        
    context = {
        'contest_page': contest,
        'page_num':pag_num,
        'trans':trans,
        'actual_url':actual_url
        }
    return render(request, "client/pages/contests.html", context)



def news(request):
    error = None
    trans = translate(language='ru')

    actual_url = request.path.split('/')[2]
    
    per_page = 12
    
    # Поиск новостей по ключевому слову
    search_posts = request.GET.get('search')

    if search_posts:
        posts = News.objects.filter(Q(Title__icontains=search_posts) | Q(Short_Description__icontains=search_posts))
    else:
        posts = News.objects.all().filter(Language = get_lang(trans=trans)).order_by("-Date_added")
        
    count=posts.count()
    
    # Получаем первую фотографию под новостями
    first_image = []
    for post in posts:
        img = PhotosNews.objects.filter(Gallery = post.Gallery).first()
        if img is None:
            error = True
        else:
            first_image.append(img.URL)
    
    current_page_news = Paginator(posts, per_page=per_page)
    current_page_img = Paginator(first_image, per_page=per_page)
    
    page_num = current_page_news.num_pages
    try:
        page = request.GET.get("page", 1)
        posts = current_page_news.page(page)
        page = request.GET.get("page", 1)
        images = current_page_img.page(page)

    except (PageNotAnInteger, TypeError):
        posts = current_page_news.page(1)
        images = current_page_img.page(1)
        
    except EmptyPage:
        posts = current_page_news.page(current_page_news.num_pages)
        images = current_page_img.page(current_page_img.num_pages)
    
    news_image_mixed = zip(posts, images)   
    context = { 
               'news_page': posts,
               'trans':trans, 
               'all_news' : news_image_mixed,
               'page_num' : page_num,
               "error" : error,
               'count':count,
               'actual_url':actual_url
               }
    return render(request, "client/pages/news.html", context)

def projects(request):
    trans = translate(language='ru')
    error = False
    search_projects = request.GET.get('search')

    actual_url = request.path.split('/')[2]

    if search_projects:
        posts = Projects.objects.filter(Q(Title__icontains=search_projects) | Q(Short_Description__icontains=search_projects))
    else:
        posts = Projects.objects.all().filter(Language = get_lang(trans=trans)).order_by("-id")

    per_page = 6
     # Получаем первую фотографию под новостями
    first_image = []
    for post in posts:
        img = PhotosProject.objects.filter(Gallery = post.Gallery_id).first()
        if img is None:
            error = True
        else:
            first_image.append(img.URL)
    
    current_page_projects = Paginator(posts, per_page=per_page)
    current_page_img = Paginator(first_image, per_page=per_page)
    
    page_num = current_page_projects.num_pages
    try:
        page = request.GET.get("page", 1)
        posts = current_page_projects.page(page)
        page = request.GET.get("page", 1)
        images = current_page_img.page(page)

    except (PageNotAnInteger, TypeError):
        posts = current_page_projects.page(1)
        images = current_page_img.page(1)
        
    except EmptyPage:
        posts = current_page_projects.page(current_page_projects.num_pages)
        images = current_page_img.page(current_page_img.num_pages)
    
    news_image_mixed = zip(posts, images)

    context = {        
        'projects_page': posts,
        'trans':trans, 
        'all_projects' : news_image_mixed,
        'page_num' : page_num,
        'error' : error,
        'actual_url':actual_url
    }
    return render(request, "client/pages/projects.html", context)


def get_news(request,title):
    trans = translate(language='ru')
    actual_url = 'news'
    news_detail = News.objects.filter(Title=title, Language = get_lang(trans=trans))
    news_title = News.objects.get(Title=title, Language=get_lang(trans=trans))
    photo = PhotosNews.objects.filter(Gallery_id=get_id_Gallery_News(title))
    context = {
        'news_detail': news_detail,
        'photo':photo,
        'news_title':news_title,
        'trans':trans,
        'actual_url':actual_url
        }
    return render(request, "client/pages/news_detail.html", context)




def investors(request):
    trans = translate(language='ru')
    actual_url = request.path.split('/')[2]

    context = {'trans':trans, 'actual_url':actual_url}
    return render(request, "client/pages/investors.html", context)

def strategy(request):
    trans = translate(language='ru')
    actual_url = request.path.split('/')[2]
    context = {'trans':trans, 'actual_url':actual_url}
    return render(request, "client/pages/strategy.html", context)

def reports(request):
    trans = translate(language='ru')
    posts = Reports.objects.order_by('-id')

    search_report = request.GET.get('search')

    actual_url = request.path.split('/')[2]

    if search_report:
        posts = Reports.objects.filter(Q(title__icontains=search_report) | Q(short_description__icontains=search_report))
    else:
        posts = Reports.objects.filter(language = get_lang(trans=trans))

    context = {'trans':trans, 'reports_all':posts, 'actual_url':actual_url}
    return render(request, "client/pages/reports.html", context)

def get_project(request,title):
    trans = translate(language='ru')
    actual_url = 'projects'

    project_detail=Projects.objects.filter(Title=title, Language=get_lang(trans=trans))
    project_title=Projects.objects.get(Title=title, Language = get_lang(trans=trans))
    photo=PhotosProject.objects.filter(Gallery_id=get_id_Gallery_project(title))
    context = {
        'project_detail': project_detail,
        'photo':photo,
        'project_title':project_title,
        'trans':trans,
        'actual_url':actual_url
        }
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

def veep(request, id):
    trans = translate(language='ru')

    actual_url = 'about_company'

    not_exist = False
    try:
        post = Management.objects.get(id=id)
    except Management.DoesNotExist:
        not_exist = True
    context = {
        'trans':trans,
        'posts':post,
        'actual_url':actual_url
        }
    return render(request, "client/pages/veep.html", context)

def vacancies(request):
    trans = translate(language='ru')
    per_page = 10

    actual_url = request.path.split('/')[2]

    vacancies = Vacancies.objects.all().filter(Language = get_lang(trans=trans)).order_by('-pub_date')
    
    paginator = Paginator(vacancies, per_page = per_page)
    page_num = paginator.num_pages
    
    try:
        page = request.GET.get("page", 1)
        vacancies = paginator.page(page)
        
    except (PageNotAnInteger, TypeError):
        vacancies = paginator.page(1)
    except EmptyPage:
        vacancies = paginator.page(page_num)
        
    context = {
               'page_vacancies': vacancies,
               'trans':trans,
               "page_num" : page_num,
               'actual_url':actual_url
               }
    return render(request, "client/pages/vacancies.html", context)

def get_vacancy(request,title):
    trans = translate(language='ru')

    vacancy_detail=Vacancies.objects.filter(title=title)
    vacancy_title=Vacancies.objects.get(title=title)

    context = {
        'vacancy_detail': vacancy_detail,
        'vacancy_title':vacancy_title,
        'trans':trans
        }
    return render(request, "client/pages/vacancy_detail.html", context)

#Страница Фотогалерея 
def gallery_page(request):
    trans = translate(language='ru')

    actual_url = request.path.split('/')[2]

    per_page = 6
    projects_photo=PhotosProject.objects.order_by('-id')
    news_photo=PhotosNews.objects.order_by('-id')
    
    paginator_projects = Paginator(projects_photo, per_page = per_page)
    paginator_news = Paginator(news_photo, per_page = per_page)

    page_num = paginator_projects.num_pages
    page_num = paginator_news.num_pages
    
    try:
        page = request.GET.get("page", 1)
        projects_photo = paginator_projects.page(page)
        news_photo = paginator_news.page(page)
        
    except (PageNotAnInteger, TypeError):
        projects_photo = paginator_projects.page(1)
        news_photo = paginator_news.page(1)
    except EmptyPage:
        projects_photo = paginator_projects.page(page_num)
        news_photo = paginator_news.page(page_num)

    news_projects_mixed = zip(projects_photo, news_photo)
        
    context = {
        'pages': news_projects_mixed,
        'trans':trans, 
        'news_photo':news_photo, 
        'projects_photo':projects_photo,
        "page_num" : page_num,
        'actual_url':actual_url
        }
    return render(request, "client/pages/gallery.html", context)


# npa 
def npa(request):
    error = False
    try:
        doc = Regulations.objects.last()
    except Exception as e:
        error = True
    context = {
        "document":doc
    }
    return render(request, 'client/pages/NPA.html', context)
# Карта сайта 
def sitemap(request):
    actual_url = request.path.split('/')[2]
    return render(request, "client/pages/sitemap.html", {'actual_url':actual_url})

# Свяжитесь с нами
def feedback(request):
    actual_url = request.path.split('/')[2]
    return render(request, "client/pages/feedback.html", {'actual_url':actual_url})

def hot_news(request):
    actual_url = request.path.split('/')[2]
    
    news_all = HotNews.objects.order_by('-id')
    error = False
    
    per_page = 1
    
    # Получаем первую фотографию под новостями
    first_image = []
    for post in news_all:
        img = HotNewsPhoto.objects.filter(gallery = post.gallery).first()
        if img is None:
            error = True
        else:
            first_image.append(img.url)
    
    current_page_news = Paginator(news_all, per_page=per_page)
    current_page_img = Paginator(first_image, per_page=per_page)
    
    page_num = current_page_news.num_pages
    try:
        page = request.GET.get("page", 1)
        posts = current_page_news.page(page)
        page = request.GET.get("page", 1)
        images = current_page_img.page(page)

    except (PageNotAnInteger, TypeError):
        posts = current_page_news.page(1)
        images = current_page_img.page(1)
        
    except EmptyPage:
        posts = current_page_news.page(current_page_news.num_pages)
        images = current_page_img.page(current_page_img.num_pages)
    
    news_image_mixed = zip(posts, images)   
    trans = translate(language='ru')
    context = { 
               'news_page': posts,
               'trans':trans, 
               'all_news' : news_image_mixed,
               'page_num' : page_num,
               "error" : error,
               'actual_url':actual_url
               }
    return render(request, "client/pages/hot_news.html", context)

def hot_news_detail(request, title):
    trans = translate(language='ru')
    news_detail=HotNews.objects.filter(title=title)
    news_title=HotNews.objects.get(title=title)
    photo=HotNewsPhoto.objects.filter(gallery_id=get_id_Gallery_HotNews(title))
    context = {
        'news_detail': news_detail,
        'photo':photo,
        'news_title':news_title,
        'trans':trans
        }
    return render(request, "client/pages/hot_news_detail.html", context)
 
def get_id_Gallery_HotNews(title):
    news_detail=HotNews.objects.filter(title=title)
    id=0
    for val in news_detail:
        id=val.gallery_id
    return id

def translate(language):
    cur_language = get_language()
    try:
        activate(language)
    finally:
        activate(cur_language)
    return cur_language

def error_400(request, exception = None):
   context = {}
   response = render(request,'client/pages/errors/400.html', context)
   response.status_code = 400
   return response

def error_403(request, exception = None):
   context = {}
   response = render(request,'client/pages/errors/403.html', context)
   response.status_code = 403
   return response

def error_404(request, exception):
   context = {}
   response = render(request,'client/pages/errors/404.html', context)
   
   response.status_code = 404
   return response


def error_500(request, exception = None):
   context = {}
   response = render(request,'client/pages/errors/500.html', context)
   response.status_code = 500
   
   return response



def send_message(request):
    sucs=True
    if request.method == 'POST':
        
        settings.EMAIL_HOST_USER='kyrgyzindustry.portal.01@gmail.com'
        settings.EMAIL_HOST_PASSWORD='jenpktauntyqbeum'

        Name = request.POST.get('name', '')
        message = request.POST.get('message', '')
        to_email = 'kyrgyzindustry.portal.01@gmail.com'
        from_email =request.POST.get('email', '')
        subject = "Сообщение от пользователей" 
        valid=validate_email(from_email,verify=True)
        if valid==True:
            try:
                body = {
                    'Name: ': "От кого: "+ Name, 
                    'from_email': "Эл.адрес: " + from_email,
                    'message': "Сообщение: " + message,
                }
                messageAll = "\n".join(body.values())
                send_mail(subject, messageAll, to_email, [from_email],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Неправильный ввод данных')
            except smtplib.SMTPException:
                messages.add_message(request, messages.ERROR, 'Ошибка при отправлении,попробуйте еще раз!')
                return redirect ('feedback')
            messages.add_message(request, messages.SUCCESS, 'Ваше сообщение отправлено!')
            return redirect ('feedback')
        else:
            messages.add_message(request, messages.ERROR, 'Неправильный эл.адрес')
            
            return redirect ('feedback')
    return redirect ('feedback')


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
            messages.error(request, "Введите Username или E-mail")
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
class AdminMain(LoginRequiredMixin, ListView):
    login_url = 'login_page'
    model = HotNews
    paginate_by = 5
    template_name = "admin/admin.html"
    #count = HotNews.objects.count()
    extra_context = {
           "is_active" : "main-panel",
          # "all_entries" : count,
    }

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
    success_url = reverse_lazy('news_create')
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
    success_message = 'Запись успешно добавлено'    


    
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

class NewsGalleryCreateView(LoginRequiredMixin,SuccessMessageMixin, NewsGalleryView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/news-gallery/newsgallery_form.html'
    success_url = reverse_lazy("newsgallery_create")
    success_message = 'Запись успеншо добавлена!'


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

class NewsImageUpdateView(LoginRequiredMixin,SuccessMessageMixin, NewsImageView, UpdateView):
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
    success_url = reverse_lazy("projectgallery_create")
    success_message = "Запись успешно добавлена!"
        

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
            messages.error(request, "Вы не сможете удалить эту галерею, так как это связано с одним или несколькими проектами или фотографиями")
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
    success_url = reverse_lazy("projects_create")
    success_message = "Запись успеншо добавлена!"
        
class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, ProjectView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/project/project_form.html"
    success_url = reverse_lazy("projects_create")
    success_message = "Запись успешно обновлено!"
    
    
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
 
    return render(request, "admin/pages/project/project_confirm_delete.html", context)      
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
    

class ContestCreateView(LoginRequiredMixin, SuccessMessageMixin, ContestView, CreateView):
    login_url = "login_page"
    template_name = "admin/pages/contests/contests_form.html"
    success_url = reverse_lazy("contests_create")
    success_message = "Запись успешно добавлена!"
        
class ContestUpdateView(LoginRequiredMixin, SuccessMessageMixin, ContestView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/contests/contests_form.html"
    success_message = "Запись успешно обновлена!"
    
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


class InterviewsView(View):
    model = Interviews
    form_class = InterviewsForm
    active_panel = "interviews-panel"
    extra_context = {
        "is_active" : active_panel,
        "active_interviews" : "active",
        "expand_interviews" : "show",
        }
    
class InterviewsListView(LoginRequiredMixin, InterviewsView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/interviews/interviews_list.html"
    

class InterviewsCreateView(LoginRequiredMixin, SuccessMessageMixin, InterviewsView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/interviews/interviews_form.html'
    success_url = reverse_lazy("interviews_create")
    success_message = "Запись успешно добавлена!"
 
class InterviewsUpdateView(LoginRequiredMixin, SuccessMessageMixin, InterviewsView, UpdateView):
    login_url = 'login_page'
    success_url = reverse_lazy("interviews_all")
    template_name = 'admin/pages/interviews/interviews_form.html'
    success_message = "Запись успешно обновлена!"
    
    
def interviews_delete(request, id):
    context = {}
    obj = get_object_or_404(Interviews, id = id)
    if request.method =="POST":
        
        try:
            # delete object
            obj.delete()
            # after deleting redirect to
            # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("interviews_all")
        except Exception as e:
            messages.error(request, "Не удалось удалить запись, повторите попытку!")
            return redirect("interviews_all")
 
    return render(request, "admin/pages/interviews/interviews_confirm_delete.html", context)  


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
    success_url = reverse_lazy("vacancies_create")
    success_message = "Запись успешно добавлена!"
        
class VacanciesUpdateView(LoginRequiredMixin, SuccessMessageMixin, VacanciesView, UpdateView):
    login_url = 'login_page'
    success_url = reverse_lazy("vacancies_all")
    template_name = 'admin/pages/vacancies/vacancies_edit.html'
    success_message = "Запись успешно обновлена!"
    

# Блоки
class BlocksView(View):
    model = Blocks
    form_class = BlocksForm
    active_panel = "blocks-panel"
    extra_context = {
        "is_active" : active_panel,
        "active_blocks" : "active",
        "expand_blocks" : "show",
        }
    
class BlocksListView(LoginRequiredMixin, BlocksView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/blocks/block_list.html"
    

class BlocksCreateView(LoginRequiredMixin, SuccessMessageMixin, BlocksView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/blocks/block_form.html'
    success_url = reverse_lazy("blocks_create")
    success_message = "Запись успешно добавлена!"
        


class BlocksUpdateView(LoginRequiredMixin, SuccessMessageMixin, BlocksView, UpdateView):
    login_url = 'login_page'
    success_url = reverse_lazy("blocks_all")
    template_name = 'admin/pages/blocks/block_edit.html'
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
    success_url = reverse_lazy("hotnewsgallery_create")
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
    obj = get_object_or_404(HotNewsPhoto, id = id)
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
    success_url = reverse_lazy("hotnews_create")
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
    success_url = reverse_lazy("hotnews_all")
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



class ReportsView(View):
    model = Reports
    form_class = ReportsForm
    active_panel = "reports-panel"
    success_url = reverse_lazy("reports_create")
    extra_context = {
        "is_active" : active_panel,
        "active_reports" : "active",
        "expand_reports" : "show",
        }
    
class ReportsListView(LoginRequiredMixin, ReportsView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/reports/reports_list.html"
    paginate_by = 10

class ReportsCreateView(LoginRequiredMixin, SuccessMessageMixin, ReportsView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/reports/reports_form.html'
    success_message = "Запись успешно Добавлена!"  

class ReportsUpdateView(LoginRequiredMixin, SuccessMessageMixin, ReportsView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/reports/reports_form.html"
    success_url = reverse_lazy("reports_all")
    success_message = "Запись успешно Обновлена!"  
    
def reports_delete(request, id):
    context = {
            "is_active" : "reports-panel",
            "active_reports" : "active",
            "expand_reports" : "show",
    }
    obj = get_object_or_404(Reports, id = id)
    if request.method =="POST":
        
        try:
            # delete object
            obj.delete()
            # after deleting redirect to
            # home page
            messages.success(request, "Запись успешно удалено!")
            return redirect("reports_all")
        except Exception as e:
            messages.error(request, "Не удалось удалить запись, повторите попытку!")
            return redirect("reports_delete")
 
    return render(request, "admin/pages/reports/reports_confirm_delete.html", context)    


class StatisticsView(View):
    model = Statistic
    form_class = StatisticsForm
    active_panel = "statistics-panel"
    success_url = reverse_lazy("statistics_create")
    extra_context = {
        "is_active" : active_panel,
        "active_statistics" : "active",
        "expand_statistics" : "show",
        }
    
class StatisticsListView(LoginRequiredMixin, StatisticsView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/statistics/statistics_list.html"
    paginate_by = 10

class StatisticsCreateView(LoginRequiredMixin, SuccessMessageMixin, StatisticsView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/statistics/statistics_form.html'
    success_message = "Запись успешно Добавлена!"  

class StatisticsUpdateView(LoginRequiredMixin, SuccessMessageMixin, StatisticsView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/statistics/statistics_form.html"
    success_url = reverse_lazy("statistics_all")
    success_message = "Запись успешно Обновлена!"


class RegulationsView(View):
    model = Regulations
    form_class = RegulationsForm
    active_panel = "regulations-panel"
    success_url = reverse_lazy("regulations_create")
    extra_context = {
        "is_active" : active_panel,
        "active_regulations" : "active",
        "expand_regulations" : "show",
        }
    
class RegulationsListView(LoginRequiredMixin, RegulationsView, ListView):
    login_url = "login_page"
    template_name = "admin/pages/regulations/regulations_list.html"
    paginate_by = 10

class RegulationsCreateView(LoginRequiredMixin, SuccessMessageMixin, RegulationsView, CreateView):
    login_url = 'login_page'
    template_name = 'admin/pages/regulations/regulations_form.html'
    success_message = "Запись успешно Добавлена!"  

class RegulationsUpdateView(LoginRequiredMixin, SuccessMessageMixin, RegulationsView, UpdateView):
    login_url = "login_page"
    template_name = "admin/pages/regulations/regulations_form.html"
    success_url = reverse_lazy("regulations_all")
    success_message = "Запись успешно Обновлена!"
 

