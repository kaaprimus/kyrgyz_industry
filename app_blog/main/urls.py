from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('img/', views.test_method, name='img'),
    path('accounts/login/', views.login_page, name='login_page'),
    path('accounts/login/success/', views.authorization, name='authorizate'),
    path('accounts/logout/', views.logout_page, name = 'logout_page'),
    path(r'admin-panel/profile/update/^', views.ProfileUpdateView.as_view(), name = 'update_profile'),
    path(r'admin-panel/profile/update/^/change_password/', views.ChangePasswordView.as_view(), name = 'change_password'),
    path('admin-panel/main/', views.AdminMain.as_view(), name='admin_panel'),
    
    # Reset password
    path("accounts/password_reset/", views.password_reset_request, name="password_reset"),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="admin/pages/user/password_reset_done.html"), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="admin/pages/user/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="admin/pages/user/password_reset_complete.html"), name='password_reset_complete'),
    # News View
    path('admin-panel/news/all/', views.NewsListView.as_view(), name='news_all'),
    path('admin-panel/news/create/', views.NewsCreateView.as_view(), name='news_create'),
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
    
    
    # Project-Image View
    path('admin-panel/image/projects/', views.ProjectImageListView.as_view(), name='projectimage_all'),
    path('admin-panel/image/projects/create/', views.ProjectImageCreateView.as_view(), name='projectimage_create'),
    path('admin-panel/image/projects/update/<int:pk>/', views.ProjectImageUpdateView.as_view(), name='projectimage_update'),
    path('admin-panel/image/projects/delete/<int:id>/', views.projectimage_delete, name='projectimage_delete'),
    
    # Project-Gallery View
    path('admin-panel/gallery/projects/', views.ProjectGalleryListView.as_view(), name='projectgallery_all'),
    path('admin-panel/gallery/projects/create/', views.ProjectGalleryCreateView.as_view(), name='projectgallery_create'),
    path('admin-panel/gallery/projects/update/<int:pk>/', views.ProjectGalleryUpdateView.as_view(), name='projectgallery_update'),
    path('admin-panel/gallery/projects/delete/<int:id>/', views.projectgallery_delete, name='projectgallery_delete'),
    
    # Projects View
    path('admin-panel/projects/', views.ProjectListView.as_view(), name='projects_all'),
    path('admin-panel/projects/create/', views.ProjectCreateView.as_view(), name='projects_create'),
    path('admin-panel/projects/update/<int:pk>/', views.ProjectUpdateView.as_view(), name='projects_update'),
    path('admin-panel/projects/delete/<int:id>/', views.projects_delete, name='projects_delete'),
    
    # Management View
    path('admin-panel/management/', views.ManagementListView.as_view(), name='management_all'),
    path('admin-panel/management/create/', views.ManagementCreateView.as_view(), name='management_create'),
    path('admin-panel/management/update/<int:pk>/', views.ManagementUpdateView.as_view(), name='management_update'),
    path('admin-panel/management/delete/<int:id>/', views.management_delete, name='management_delete'),
    
    
    # Vacancies View
    path('admin-panel/vacancies/', views.VacanciesListView.as_view(), name='vacancies_all'),
    path('admin-panel/vacancies/create/', views.VacanciesCreateView.as_view(), name='vacancies_create'),
    path('admin-panel/vacancies/update/<int:pk>/', views.VacanciesUpdateView.as_view(), name='vacancies_update'),
    path('admin-panel/vacancies/delete/<int:id>/', views.vacancies_delete, name='vacancies_delete'),
    
    # Blocks View
    path('admin-panel/blocks/', views.BlocksListView.as_view(), name='blocks_all'),
    path('admin-panel/blocks/create/', views.BlocksCreateView.as_view(), name='blocks_create'),
    path('admin-panel/blocks/update/<int:pk>/', views.BlocksUpdateView.as_view(), name='blocks_update'),    

    # HotNews - Gallery  View
    path('admin-panel/gallery/hotnews/', views.HotNewsGalleryListView.as_view(), name='hotnewsgallery_all'),
    path('admin-panel/gallery/hotnews/create/', views.HotNewsGalleryCreateView.as_view(), name='hotnewsgallery_create'),
    path('admin-panel/gallery/hotnews/update/<int:pk>/', views.HotNewsGalleryUpdateView.as_view(), name='hotnewsgallery_update'),
    path('admin-panel/gallery/hotnews/delete/<int:id>/', views.hotnewsgallery_delete, name='hotnewsgallery_delete'),
    
    # HotNews - Image  View
    path('admin-panel/image/hotnews/', views.HotNewsImageListView.as_view(), name='hotnewsimage_all'),
    path('admin-panel/image/hotnews/create/', views.HotNewsImageCreateView.as_view(), name='hotnewsimage_create'),
    path('admin-panel/image/hotnews/update/<int:pk>/', views.HotNewsImageUpdateView.as_view(), name='hotnewsimage_update'),
    path('admin-panel/image/hotnews/delete/<int:id>/', views.hotnewsimage_delete, name='hotnewsimage_delete'),
    
    # HotNews View
    path('admin-panel/hotnews/', views.HotNewsListView.as_view(), name='hotnews_all'),
    path('admin-panel/hotnews/create/', views.HotNewsCreateView.as_view(), name='hotnews_create'),
    path('admin-panel/hotnews/update/<int:pk>/', views.HotNewsUpdateView.as_view(), name='hotnews_update'),
    path('admin-panel/hotnews/delete/<int:id>/', views.hotnews_delete, name='hotnews_delete'),

    # Interviews View
    path('admin-panel/interviews/', views.InterviewsListView.as_view(), name='interviews_all'),
    path('admin-panel/interviews/create/', views.InterviewsCreateView.as_view(), name='interviews_create'),
    path('admin-panel/interviews/update/<int:pk>/', views.InterviewsUpdateView.as_view(), name='interviews_update'),
    path('admin-panel/interviews/delete/<int:id>/', views.interviews_delete, name='interviews_delete'),

    # Report View
    path('admin-panel/reports/', views.ReportsListView.as_view(), name='reports_all'),
    path('admin-panel/reports/create/', views.ReportsCreateView.as_view(), name='reports_create'),
    path('admin-panel/reports/update/<int:pk>/', views.ReportsUpdateView.as_view(), name='reports_update'),
    path('admin-panel/reports/delete/<int:id>/', views.reports_delete, name='reports_delete'),
    
    # Static Pages
    path('about_company', views.about_company, name='about_company'),
    path('about_us_full_info', views.about_us_full_info, name='about_us_full_info'),
    path('president', views.president, name='president'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('gallery_page/<int:number_page>/', views.gallery_page, name='gallery'),
    path('news/', views.news, name='news'),
    path('projects/', views.projects, name='projects'),
    path('invest/', views.investors, name='invest'),
    path('strategy/', views.strategy, name='strategy'),
    path('reports/', views.reports, name='reports'),
    path('contests', views.contests, name='contests'),
    path('send_message/', views.send_message),
    path('news_detail/<str:title>', views.get_news, name='news_detail'),
    path('project_detail/<str:title>', views.get_project, name='project_detail'),
    path('veep/<int:id>', views.veep, name='veep'),
    path('advisor/<int:id>', views.veep, name='advisors'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('interviews/', views.interviews, name='interviews'),
    path('vacancy_detail/<str:title>', views.get_vacancy, name='vacancy_detail'),
    path('page_vacancy/<int:number_page>/', views.news, name='vacancy'),
    path('detail_news/<str:title>', views.get_news, name='detail_news'),
    path('page_news/<int:number_page>/', views.news, name='news'),
    path('page_contest/<int:number_page>/', views.contests, name='contests'),
    path('page_project/<int:number_page>/', views.projects, name='projects'),
    path('sitemap/', views.sitemap, name = 'sitemap'),
    path('feedback', views.feedback, name = 'feedback'),
    path('block_detail/<str:titleblock>', views.get_block_detail, name='block_detail'),
    # Новые добавленные страницы
    path('main_events/', views.hot_news, name='hot_news'),
    path('main_events_detail/<str:title>', views.hot_news_detail, name='hot_news_detail'),
    path('not/', views.error_500, name='not'),
    
]
