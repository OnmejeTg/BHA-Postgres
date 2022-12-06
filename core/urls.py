from django.urls import path
from .import views

urlpatterns = [

    path('', views.index, name='index'),

    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),

    path('announcement/', views.announcement, name='announcement'),

    path('parent/', views.view_parent, name='view_parent'),
    path('parent/add/', views.add_parent, name='add_parent'),
    path('parent/search/', views.search_parent, name='search_parent'),
    path('parent/detail/<str:id_parent>',
         views.parent_detail, name='parent_detail'),
    path('parent/edit/<str:id_parent>', views.edit_parent, name='edit_parent'),

    path('staff/', views.view_staff, name='view_staff'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/detail/<str:id_staff>', views.staff_detail, name='staff_detail'),
    path('staff/edit/<str:id_staff>', views.edit_staff, name='edit_staff'),

    path('pupil/', views.pupil, name='active'),
    path('pupil-withdrawn/', views.withdrawn, name='withdrawn'),
    path('pupil-graduated/', views.graduated, name='graduated'),
    path('pupil/add', views.add_pupil, name='add_pupil'),
    path('pupil/view_by_class/', views.view_pupil_by_class,
         name='view_pupil_by_class'),
    path('pupil/search', views.search_pupil, name='search_pupil'),
    path('pupil/edit/<str:id_pupil>', views.edit_pupil, name='edit_pupil'),
    path('pupil/detail/<str:id_pupil>', views.pupil_detail, name='pupil_detail'),

    path('fee/', views.fee, name='fee'),
    path('check/fee/', views.check_fee, name='check_fee'),
    path('fee/defaulter/', views.fee_defaulter, name='fee_defaulter'),
    path('pay/<str:id_pupil>', views.pay_id, name='pay_id'),
    path('pay/', views.pay, name='pay'),
    path('pay/action/', views.pay_action, name='pay_action'),
]
