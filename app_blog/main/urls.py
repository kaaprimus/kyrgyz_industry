from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.login_page, name='login_page'),
    path('accounts/login/success/', views.authorization, name='authorizate'),
    path('accounts/logout/', views.logout_page, name = 'logout_page'),
    path('detail/', views.detail, name='detail'),
    path('admin-panel/main/', views.admin_index_page, name='admin_panel'),
    # News View
    path('admin-panel/news/all/', views.NewsListView.as_view(), name='news_all'),
    path('admin-panel/news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('admin-panel/news/detail/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('admin-panel/news/update/<int:pk>/', views.NewsUpdateView.as_view(), name='news_update'),
    path('admin-panel/news/delete/<int:id>/', views.news_delete, name='news_delete'),
    
    # News Gallery View
    path('admin-panel/gallery/news/', views.NewsGalleryListView.as_view(), name='newsgallery_all'),
    path('admin-panel/gallery/news/create/', views.NewsGalleryCreateView.as_view(), name='newsgallery_create'),
    path('admin-panel/gallery/news/update/<int:pk>/', views.NewsGalleryUpdateView.as_view(), name='newsgallery_update'),
    path('admin-panel/gallery/news/delete/<int:id>/', views.newsgallery_delete, name='newsgallery_delete'),
    
    # News Image View
    path('admin-panel/image/news/', views.NewsImageListView.as_view(), name='newsimage_all'),
    path('admin-panel/image/news/create/', views.NewsImageCreateView.as_view(), name='newsimage_create'),
    path('admin-panel/image/news/update/<int:pk>/', views.NewsImageUpdateView.as_view(), name='newsimage_update'),
    path('admin-panel/image/news/delete/<int:id>/', views.newsimage_delete, name='newsimage_delete'),
    
    
    # Contests View
    path('admin-panel/contests/', views.ContestListView.as_view(), name='contests_all'),
    path('admin-panel/contests/create/', views.ContestCreateView.as_view(), name='contests_create'),
    path('admin-panel/contests/update/<int:pk>/', views.ContestUpdateView.as_view(), name='contests_update'),
    path('admin-panel/contests/delete/<int:id>/', views.contests_delete, name='contests_delete'),

    # Vacancies View
    path('admin-panel/vacancies/all/', views.VacanciesListView.as_view(), name='vacancies_all'),
    path('admin-panel/vacancies/create/', views.VacanciesCreateView.as_view(), name='vacancies_create'),
    path('admin-panel/vacancies/update/<int:pk>/', views.VacanciesUpdateView.as_view(), name='vacancies_update'),
    path('admin-panel/vacancies/delete/<int:id>/', views.vacancies_delete, name='vacancies_delete'),

    # Static Pages
    path('about_company', views.about_company, name='about_company'),
    path('president', views.president, name='president'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('gallery_page/<int:number_page>/', views.gallery_page, name='gallery'),
    path('news/', views.news, name='news'),
    path('projects/', views.projects, name='projects'),
    path('contests', views.contests, name='contests'),
    path('send_message/', views.send_message),
    path('news_detail/<str:title>', views.get_news, name='news_detail'),
    path('project_detail/<str:title>', views.project_detail, name='project_detail'),
    path('veep', views.veep, name='veep'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('vacancy_detail/<str:title>', views.get_vacancy, name='vacancy_detail'),
    path('page_vacancy/<int:number_page>/', views.news, name='vacancy'),
    path('detail_news/<str:title>', views.get_news, name='detail_news'),
    path('page_news/<int:number_page>/', views.news, name='news'),
    path('page_contest/<int:number_page>/', views.contests, name='contests'),
    path('page_project/<int:number_page>/', views.projects, name='projects'),
    path('documents_npa', views.npa, name='documents_npa'),
]
