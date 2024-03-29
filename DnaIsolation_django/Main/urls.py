from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.orders, name='main-orders'),
    path('order/select_company', views.orderSelectCompany, name='order-select-company'),
    path('order/create/<int:pk>/', views.orderCreate, name='order-create'),
    path('order/create/new_company', views.orderCreateNewCompany, name='order-create-newcompany'),
    path('order/detail/<int:pk>/', views.orderDetailView, name='order-details'),
    path('order/delete_confirm/<int:pk>/', views.orderDeleteConfirm, name='order-delete-confirm'),
    path('order/delete/<int:pk>/', views.orderDelete, name='order-delete'),
    path('order/edit/<int:pk>/', views.orderEdit, name='order-edit'),
    path('order/edit_company_confirm/<int:pk>/', views.orderEditCompanyCheck, name='order-edit-company-check'),

    path('files', views.files, name='main-files'),
    path('edit_company/<int:pk>/', views.orderEditCompany, name='edit-company'),
    path('download_linked/<int:pk>/', views.downloadLinkedFile, name='download-linked'),
    path('download/<int:pk>/', views.downloadSimpleFile, name='download'),
    path('delete_file_confirm/<int:pk>', views.fileDeleteConfirm, name='file-delete-confirm'),
    path('delete_file/<int:pk>/', views.fileDelete, name='file-delete'),
    path('file/add/', views.fileAdd, name='file-add'),

    path('materials', views.materials, name='main-materials'),
    path('material/create', views.materialCreate, name='material-create'),
    path('material/detail/<int:pk>/', views.materialDetailView, name='material-details'),
    path('material/delete_confirm/<int:pk>/', views.materialDeleteConfirm, name='material-delete-confirm'),
    path('material/delete/<int:pk>/', views.materialDelete, name='material-delete'),
    path('material/edit/<int:pk>/', views.materialEdit, name='material-edit'),
    path('material/edit_company_confirm/<int:pk>/', views.materialEditCompanyCheck, name='material-edit-company-check'),

    path('material/add_operation/<int:pk>/', views.materialAddOperation, name='material-add-operation'),
    path('material/operation_list/<int:pk>/', views.materialOperationList, name='material-operation-list'),

    path('material/delete_operation/<int:mat_pk>/<int:op_id>/', views.materialDeleteOperation, name='material-delete-operation'),
    path('material/archive_operation/<int:mat_pk>/<int:op_id>/', views.materialArchiveOperation, name='material-archive-operation'),
    path('material/dearchive_operation/<int:mat_pk>/<int:op_id>/', views.materialDearchiveOperation, name='material-dearchive-operation'),
    path('material/edit_operation/<int:mat_pk>/<int:op_id>/', views.materialEditOperation, name='material-edit-operation'),

    path('operation_log', views.operationLog, name='main-operations'),
]