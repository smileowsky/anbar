from django.urls import path
from . import views

urlpatterns = [


    path('loader', views.loader, name='loader'),
     
    path('', views.home, name='home'),
    path('main', views.main, name='main'),


    path('user_register', views.user_register, name='user_register'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),

    path('user_profile', views.user_profile, name='user_profile'),
    path('user_profile_update', views.user_profile_update,
         name='user_profile_update'),

    path('brand', views.brand, name='brand'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('delete_config/<int:id>', views.delete_config, name='delete_config'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name='update'),

    path('client', views.client, name='client'),
    path('client_delete/<int:id>', views.client_delete, name='client_delete'),
    path('client_delete_config/<int:id>',
         views.client_delete_config, name='client_delete_config'),
    path('client_edit/<int:id>', views.client_edit, name='client_edit'),
    path('client_update/<int:id>', views.client_update, name='client_update'),

    path('expens', views.expens, name='expens'),
    path('expens_delete/<int:id>', views.expens_delete, name='expens_delete'),
    path('expens_delete_config/<int:id>',
         views.expens_delete_config, name='expens_delete_config'),
    path('expens_edit/<int:id>', views.expens_edit, name='expens_edit'),
    path('expens_update/<int:id>', views.expens_update, name='expens_update'),

    path('products', views.products, name='products'),
    path('products_delete/<int:id>', views.products_delete, name='products_delete'),
    path('products_delete_config/<int:id>',
         views.products_delete_config, name='products_delete_config'),
    path('products_edit/<int:id>', views.products_edit, name='products_edit'),
    path('products_update/<int:id>', views.products_update, name='products_update'),

    path('orders', views.orders, name='orders'),
    path('orders_delete/<int:id>', views.orders_delete, name='orders_delete'),
    path('orders_delete_config/<int:id>',
         views.orders_delete_config, name='orders_delete_config'),
    path('orders_edit/<int:id>', views.orders_edit, name='orders_edit'),
    path('orders_update/<int:id>', views.orders_update, name='orders_update'),
    path('orders_tesdiq/<int:id>', views.orders_tesdiq, name='orders_tesdiq'),
    path('orders_cancel/<int:id>', views.orders_cancel, name='orders_cancel'),

    path('departments', views.departments, name='departments'),
    path('department_del/<int:id>', views.department_del, name='department_del'),
    path('department_del_conf/<int:id>',
         views.department_del_conf, name='department_del_conf'),
    path('department_edit/<int:id>', views.department_edit, name='department_edit'),
    path('department_update/<int:id>',
         views.department_update, name='department_update'),

    path('positions', views.positions, name='positions'),
    path('position_del/<int:id>', views.position_del, name='position_del'),
    path('position_del_conf/<int:id>',
         views.position_del_conf, name='position_del_conf'),
    path('position_edit/<int:id>', views.position_edit, name='position_edit'),
    path('position_update/<int:id>', views.position_update, name='position_update'),

    path('staff', views.staff, name='staff'),
    path('staff_delete/<int:id>', views.staff_delete, name='staff_delete'),
    path('staff_del_conf/<int:id>', views.staff_del_conf, name='staff_del_conf'),
    path('staff_edit/<int:id>', views.staff_edit, name='staff_edit'),
    path('staff_update/<int:id>', views.staff_update, name='staff_update'),

    path('documents/<int:staf_id>', views.documents, name='documents'),

    path('document_delete/<int:doc_id>',
         views.document_delete, name='document_delete'),
    path('doc_del_conf/<int:doc_d_id>', views.doc_del_conf, name='doc_del_conf'),
    path('doc_edit/<int:doc_id>', views.doc_edit, name='doc_edit'),
    path('doc_update/<int:doc_id>', views.doc_update, name='doc_update'),

    path('assignments', views.assignments, name='assignments'),
    path('assignment_del/<int:assign_id>',
         views.assignments_del, name='assignment_del'),
    path('assignment_del_conf/<int:assign_id>',
         views.assignments_del_conf, name='assignment_del_conf'),
    path('assignment_edit/<int:assign_id>',
         views.assignment_edit, name='assignment_edit'),
    path('assignment_update<int:assign_id>',
         views.assignment_update, name='assignment_update'),
    path('assignment_approve/<int:assign_id>',
         views.assignments_approve, name='assignment_approve'),
    path('assignment_cancel/<int:assign_id>',
         views.assignment_cancel, name='assignment_cancel'),

    path('supplier', views.supplier, name='supplier'),
    path('supplier_delete/<int:supp_id>',
         views.supplier_delete, name='supplier_delete'),
    path('supplier_del_conf/<int:supp_id>',
         views.supplier_del_conf, name='supplier_del_conf'),
    path('supplier_edit/<int:supp_id>',
         views.supplier_edit, name='supplier_edit'),
    path('supplier_update/<int:supp_id>',
         views.supplier_update, name='supplier_update'),
]
