# myapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import mark_notification_as_read

urlpatterns = [
    # URL CHUNG
    path('', views.home, name='home'),
    # XÁC THỰC
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('chat/send/', views.send_chat_message, name='send_chat_message'),
    path('chat/get/', views.get_chat_messages, name='get_chat_messages'),
    # urls.py
    path('chat/mark_read/', views.mark_chat_as_read, name='mark_chat_as_read'),
    path('notification/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark_notification_as_read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),

    
    # TRƯỞNG PHÒNG
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/products/', views.manager_product_list, name='manager_product_list'),
    path('manager/products/update_status/<int:product_id>/', views.manager_update_status, name='manager_update_status'),
    path('manager/products/<int:product_id>/feedbacks/', views.manager_products_feedback_list, name='manager_products_feedback_list'),
    path('manager/products/<int:product_id>/feedbacks/create', views.manager_create_feedback, name='manager_create_feedback'),
    
      # THƯ KÝ
    path('secretary/dashboard/', views.secretary_dashboard, name='secretary_dashboard'),
    path('secretary/products/create/', views.secretary_create_product, name='secretary_create_product'),
    path('secretary/products/', views.secretary_product_list, name='secretary_product_list'),
    path('secretary/products/<int:product_id>/', views.secretary_product_detail, name='secretary_product_detail'),
    path('secretary/products/<int:product_id>/edit_product/', views.secretary_edit_product, name='secretary_edit_product'),
    path('secretary/products/<int:product_id>/designrequests/', views.secretary_design_request_list, name='secretary_design_request_list'),
    path('secretary/designrequests/<int:request_id>/delete/', views.secretary_delete_design_request, name='secretary_delete_design_request'),
    path('secretary/feedbacks/<int:request_id>/', views.secretary_feedback_list, name='secretary_feedback_list'),
    path('secretary/designrequest/update_status/<int:request_id>/', views.secretary_update_status, name='secretary_update_status'),
    path('secretary/products/<int:product_id>/feedbacks/', views.secretary_products_feedback_list, name='secretary_products_feedback_list'),
    path('secretary/designrequests/<int:request_id>/feedbacks/', views.secretary_designrequests_feedback_list, name='secretary_designrequests_feedback_list'),
    path('secretary/designrequests/<int:request_id>/feedbacks/create', views.secretary_create_feedback, name='secretary_create_feedback'),
     
     # NGƯỜI THIẾT KẾ
    path('designer/dashboard/', views.designer_dashboard, name='designer_dashboard'),
    path('designer/products/', views.designer_product_list, name='designer_product_list'),
    path('designer/products/<int:product_id>/designrequests/', views.designer_design_request_list, name='designer_designrequests_list'),
    path('designer/products/<int:product_id>/designrequests/create/', views.designer_create_design_request, name='designer_create_design_request'),
    path('designer/designrequests/<int:request_id>/edit/', views.designer_edit_design_request, name='designer_edit_design_request'),
    path('designer/designrequests/<int:request_id>/delete/', views.designer_delete_design_request, name='designer_delete_design_request'),
     path('designer/designrequests/<int:request_id>/feedbacks/', views.designer_designrequests_feedback_list, name='designer_designrequests_feedback_list'),
]
