# myapp/views.py
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import CustomUser, Notification
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, DesignRequest, ProductFeedback, RequestFeedback
from .forms import ProductForm, DesignRequestForm
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DesignRequestForm
from .models import Product, DesignRequest
import sys
import io
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def home(request):
    return HttpResponse("Hello, World!")

logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('pass')

        logger.debug(f"Login attempt with username: {username}")

        # Kiểm tra xem username và password có được cung cấp không
        if not username or not password:
            messages.error(request, 'Vui lòng nhập đầy đủ tài khoản và mật khẩu.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            logger.debug(f"User {username} authenticated successfully")
            login(request, user)
            messages.success(request, 'Đăng nhập thành công!')

            if user.role == 'Thư ký':
                return redirect('secretary_dashboard')
            elif user.role == 'Người thiết kế':
                return redirect('designer_dashboard')
            elif user.role == 'Trưởng phòng':
                return redirect('manager_dashboard')
        else:
            logger.warning(f"Invalid login attempt for {username}")
            messages.error(request, 'Đăng nhập thất bại. Tài khoản hoặc mật khẩu không đúng.')
            return redirect('login')

    return render(request, 'myapp/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = CustomUser.objects.create_user(username=username, password=password, role=role)

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Tạo tài khoản thành công!')  # Thêm thông báo thành công

        if role == 'Thư ký':
            return redirect('secretary_dashboard')
        elif role == 'Người thiết kế':
            return redirect('designer_dashboard')
        elif role == 'Trưởng phòng':
            return redirect('manager_dashboard')

    return render(request, 'myapp/register.html')


def logout_view(request):
    logout(request)  
    messages.success(request, 'Đăng xuất thành công!')
    return redirect('login') 



from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def role_required(allowed_role):
    def decorator(view_func):
        @login_required  # Đảm bảo người dùng đã đăng nhập
        def wrapper(request, *args, **kwargs):
            if request.user.role != allowed_role:
                # Nếu vai trò không khớp, trả về lỗi 403 hoặc chuyển hướng
                messages.error(request, f"Bạn không có quyền truy cập vào trang này. Vai trò của bạn là '{request.user.role}'.")
                
                # Chuyển hướng người dùng về dashboard phù hợp với vai trò của họ
                if request.user.role == 'Thư ký':
                    return redirect('secretary_dashboard')
                elif request.user.role == 'Người thiết kế':
                    return redirect('designer_dashboard')
                elif request.user.role == 'Trưởng phòng':
                    return redirect('manager_dashboard')
                else:
                    # Nếu không có vai trò hợp lệ, chuyển về trang đăng nhập
                    return redirect('login')
            
            # Nếu vai trò khớp, cho phép truy cập view
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@role_required('Người thiết kế')
def designer_dashboard(request):
    try:
        # Lấy ngày hiện tại nếu không có ngày được chọn
        selected_date = request.GET.get('date', timezone.now().date().isoformat())
        date = parse_date(selected_date)

        if not date:
            date = timezone.now().date()

        num_designers = CustomUser.objects.filter(role='Người thiết kế').count()
        num_managers = CustomUser.objects.filter(role='Trưởng phòng').count()
        num_secretary = CustomUser.objects.filter(role='Thư ký').count()
        num_products = Product.objects.count()

        num_products_dang_thiet_ke = Product.objects.filter(
            status='Đang được thiết kế', created_at__date=date
        ).count()
        num_products_dang_chua_phat_hanh = Product.objects.filter(
            status='Chờ phát hành', created_at__date=date
        ).count()
        num_products_da_huy = Product.objects.filter(
            status='Đã huỷ', created_at__date=date
        ).count()
        num_products_da_phat_hanh = Product.objects.filter(
            status='Đã phát hành', created_at__date=date
        ).count()

        # Tổng số sản phẩm theo trạng thái (không lọc theo ngày)
        total_dang_thiet_ke = Product.objects.filter(status='Đang được thiết kế').count()
        total_dang_chua_phat_hanh = Product.objects.filter(status='Chờ phát hành').count()
        total_da_huy = Product.objects.filter(status='Đã huỷ').count()
        total_da_phat_hanh = Product.objects.filter(status='Đã phát hành').count()
        unread_count = request.user.notifications.filter(is_read=False).count()
        unread_messages = ChatMessage.objects.filter(is_read=False).exclude(sender=request.user).count()

        notifications = request.user.notifications.all().order_by('-created_at')

        notifications_data = [
            {
                'notification_id': notification.notification_id,
                'message': notification.message,
                'url': notification.url,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),  # Chuyển datetime thành chuỗi
            }
            for notification in notifications
        ]

        context = {
            'current_page': 'dashboard',
            'num_designers': num_designers,
            'num_managers': num_managers,
            'num_secretary': num_secretary,
            'num_products': num_products,
            'num_products_dang_thiet_ke': num_products_dang_thiet_ke,
            'num_products_dang_chua_phat_hanh': num_products_dang_chua_phat_hanh,
            'num_products_da_huy': num_products_da_huy,
            'num_products_da_phat_hanh': num_products_da_phat_hanh,
            'total_dang_thiet_ke': total_dang_thiet_ke,
            'total_dang_chua_phat_hanh': total_dang_chua_phat_hanh,
            'total_da_huy': total_da_huy,
            'total_da_phat_hanh': total_da_phat_hanh,
            'unread_count': unread_count,
            'notifications': notifications_data,
            'unread_chat_count': unread_messages,
        }
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Kiểm tra AJAX request
            return JsonResponse(context)
        return render(request, 'myapp/designer/dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in designer_dashboard: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@role_required('Trưởng phòng')
def manager_dashboard(request):
    try:
        # Lấy ngày hiện tại nếu không có ngày được chọn
        selected_date = request.GET.get('date', timezone.now().date().isoformat())
        date = parse_date(selected_date)

        if not date:
            date = timezone.now().date()

        num_designers = CustomUser.objects.filter(role='Người thiết kế').count()
        num_managers = CustomUser.objects.filter(role='Trưởng phòng').count()
        num_secretary = CustomUser.objects.filter(role='Thư ký').count()
        num_products = Product.objects.count()

        num_products_dang_thiet_ke = Product.objects.filter(
            status='Đang được thiết kế', created_at__date=date
        ).count()
        num_products_dang_chua_phat_hanh = Product.objects.filter(
            status='Chờ phát hành', created_at__date=date
        ).count()
        num_products_da_huy = Product.objects.filter(
            status='Đã huỷ', created_at__date=date
        ).count()
        num_products_da_phat_hanh = Product.objects.filter(
            status='Đã phát hành', created_at__date=date
        ).count()

        # Tổng số sản phẩm theo trạng thái (không lọc theo ngày)
        total_dang_thiet_ke = Product.objects.filter(status='Đang được thiết kế').count()
        total_dang_chua_phat_hanh = Product.objects.filter(status='Chờ phát hành').count()
        total_da_huy = Product.objects.filter(status='Đã huỷ').count()
        total_da_phat_hanh = Product.objects.filter(status='Đã phát hành').count()
        unread_count = request.user.notifications.filter(is_read=False).count()
        unread_messages = ChatMessage.objects.filter(is_read=False).exclude(sender=request.user).count()

        notifications = request.user.notifications.all().order_by('-created_at')

        notifications_data = [
            {
                'notification_id': notification.notification_id,
                'message': notification.message,
                'url': notification.url,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),  # Chuyển datetime thành chuỗi
            }
            for notification in notifications
        ]

        context = {
            'current_page': 'dashboard',
            'num_designers': num_designers,
            'num_managers': num_managers,
            'num_secretary': num_secretary,
            'num_products': num_products,
            'num_products_dang_thiet_ke': num_products_dang_thiet_ke,
            'num_products_dang_chua_phat_hanh': num_products_dang_chua_phat_hanh,
            'num_products_da_huy': num_products_da_huy,
            'num_products_da_phat_hanh': num_products_da_phat_hanh,
            'total_dang_thiet_ke': total_dang_thiet_ke,
            'total_dang_chua_phat_hanh': total_dang_chua_phat_hanh,
            'total_da_huy': total_da_huy,
            'total_da_phat_hanh': total_da_phat_hanh,
            'unread_count': unread_count,
            'notifications': notifications_data,
            'unread_chat_count': unread_messages,
        }
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Kiểm tra AJAX request
            return JsonResponse(context)
        return render(request, 'myapp/manager/dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in manager_dashboard: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# Thư ký
@role_required('Thư ký')
def secretary_dashboard(request):
    try:
        # Lấy ngày hiện tại nếu không có ngày được chọn
        selected_date = request.GET.get('date', timezone.now().date().isoformat())
        date = parse_date(selected_date)

        if not date:
            date = timezone.now().date()

        # Tính toán thống kê dựa trên ngày được chọn
        num_designers = CustomUser.objects.filter(role='Người thiết kế').count()
        num_managers = CustomUser.objects.filter(role='Trưởng phòng').count()
        num_secretary = CustomUser.objects.filter(role='Thư ký').count()
        num_products = Product.objects.count()

        num_products_dang_thiet_ke = Product.objects.filter(
            status='Đang được thiết kế', created_at__date=date
        ).count()
        num_products_dang_chua_phat_hanh = Product.objects.filter(
            status='Chờ phát hành', created_at__date=date
        ).count()
        num_products_da_huy = Product.objects.filter(
            status='Đã huỷ', created_at__date=date
        ).count()
        num_products_da_phat_hanh = Product.objects.filter(
            status='Đã phát hành', created_at__date=date
        ).count()

        # Tổng số sản phẩm theo trạng thái (không lọc theo ngày)
        total_dang_thiet_ke = Product.objects.filter(status='Đang được thiết kế').count()
        total_dang_chua_phat_hanh = Product.objects.filter(status='Chờ phát hành').count()
        total_da_huy = Product.objects.filter(status='Đã huỷ').count()
        total_da_phat_hanh = Product.objects.filter(status='Đã phát hành').count()
        unread_count = request.user.notifications.filter(is_read=False).count()
        unread_messages = ChatMessage.objects.filter(is_read=False).exclude(sender=request.user).count()

        notifications = request.user.notifications.all().order_by('-created_at')
        notifications_data = [
            {
                'notification_id': notification.notification_id,
                'message': notification.message,
                'url': notification.url,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),  # Chuyển datetime thành chuỗi
            }
            for notification in notifications
        ]
        print(f"User: {request.user.username}, Notifications count: {notifications.count()}")

        context = {
            'current_page': 'dashboard',
            'num_designers': num_designers,
            'num_managers': num_managers,
            'num_secretary': num_secretary,
            'num_products': num_products,
            'num_products_dang_thiet_ke': num_products_dang_thiet_ke,
            'num_products_dang_chua_phat_hanh': num_products_dang_chua_phat_hanh,
            'num_products_da_huy': num_products_da_huy,
            'num_products_da_phat_hanh': num_products_da_phat_hanh,
            'total_dang_thiet_ke': total_dang_thiet_ke,
            'total_dang_chua_phat_hanh': total_dang_chua_phat_hanh,
            'total_da_huy': total_da_huy,
            'total_da_phat_hanh': total_da_phat_hanh,
            'unread_count': unread_count,
            'notifications': notifications,
            'notifications': notifications_data,
            'unread_chat_count': unread_messages,
        }

        print(f"Date: {date}, Stats: {context}")  # Debug

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Kiểm tra AJAX request
            return JsonResponse(context)
        return render(request, 'myapp/secretary/dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in secretary_dashboard: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@role_required('Thư ký')
def secretary_product_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    # Bắt đầu với tất cả sản phẩm
    products = Product.objects.all()

    # Lọc theo search_query nếu có
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Lọc theo status_filter nếu có
    if status_filter:
        products = products.filter(status=status_filter)

    unread_count = request.user.notifications.filter(is_read=False).count()
    notifications = request.user.notifications.all().order_by('-created_at')

    # Kiểm tra nếu là yêu cầu AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = [
            {
                'product_id': product.product_id,
                'name': product.name,
                'status': product.get_status_display(),
                'progress': product.progress,
                'created_at': product.created_at.strftime('%d/%m/%Y'),
            }
            for product in products
        ]
        return JsonResponse({
            'products': products_data,
            'unread_count': unread_count,
        })

    context = {
        'current_page': 'product_list',
        'products': products,
        'search_query': search_query,
        'unread_count': unread_count,
        'notifications': notifications,
        'status_filter': status_filter,
    }
    return render(request, 'myapp/secretary/products/list.html', context)


@role_required('Thư ký')
def secretary_product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    design_requests = DesignRequest.objects.filter(product=product)
    feedbacks = Feedback.objects.filter(request__product=product)
    return render(request, 'myapp/secretary/product_detail.html', {
        'product': product,
        'design_requests': design_requests,
        'feedbacks': feedbacks,
    })


@role_required('Thư ký')
def secretary_create_product(request):
    designers = CustomUser.objects.filter(role='Người thiết kế')
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.created_by = request.user 
            designer_id = form.cleaned_data.get('designer')
            
            if designer_id:
                new_product.designer = CustomUser.objects.get(user_id=designer_id)
            
            # Cập nhật tiến độ dựa trên trạng thái ban đầu
            new_product.status = 'Đang được thiết kế'  # Trạng thái mặc định
            new_product.progress = 25  # Tiến độ ban đầu là 25%
            
            new_product.save() 
            # Tạo thông báo cho designer
            if designer_id:
                new_product.designer = CustomUser.objects.get(user_id=designer_id)
                notification_url = reverse('designer_create_design_request', kwargs={'product_id': new_product.product_id})
                Notification.objects.create(
                    recipient=new_product.designer,
                    message=f"Đã nhận được bản yêu cầu thiết kế từ Thư ký cho sản phẩm '{new_product.name}'.",
                    url=notification_url
            )
            return redirect('secretary_product_list')  
    else:
        form = ProductForm()

    return render(request, 'myapp/secretary/products/create.html', {'form': form, 'designers': designers})


@role_required('Thư ký')
def secretary_edit_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    designers = CustomUser.objects.filter(role='Người thiết kế')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            updated_product.created_by = request.user 
            designer_id = form.cleaned_data.get('designer')
            if designer_id:
                updated_product.designer = CustomUser.objects.get(user_id=designer_id)
            updated_product.save() 
            return redirect('secretary_product_list')  
    else:
        form = ProductForm(instance=product)

    return render(request, 'myapp/secretary/products/edit.html', {'form': form, 'product': product, 'designers': designers})


@role_required('Thư ký')
def secretary_design_request_list(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    design_requests = DesignRequest.objects.filter(product=product)

    return render(request, 'myapp/secretary/design/list.html', {
        'product': product,
        'design_requests': design_requests
    })

@role_required('Thư ký')
def secretary_delete_design_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)
    try:
        design_request.delete()
        logger.info(f"Design request {request_id} deleted successfully by {request.user.username}")
        return redirect('secretary_product_list')  
    except Exception as e:
        logger.error(f"Error deleting design request {request_id} by {request.user.username}: {e}")
        return HttpResponse("An error occurred while deleting the design request.", status=500)


@role_required('Thư ký')
def secretary_feedback_list(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)
    
    feedbacks = RequestFeedback.objects.filter(request=design_request)
    
    return render(request, 'myapp/secretary/feedback/list.html', {
        'design_request': design_request,
        'feedbacks': feedbacks
    })


from django.shortcuts import render, get_object_or_404, redirect
from .forms import RequestFeedbackForm
from .models import DesignRequest, RequestFeedback
from django.contrib.auth.decorators import login_required

@role_required('Thư ký')
def secretary_create_feedback(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)

    if request.method == 'POST':
        form = RequestFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.request = design_request 
            feedback.sender = request.user    
            feedback.receiver = design_request.designer  
            feedback.save()
            
            # Tạo thông báo cho Người thiết kế
            product = design_request.product  # Lấy sản phẩm liên quan đến yêu cầu thiết kế
            notification_url = reverse('designer_designrequests_feedback_list', kwargs={'request_id': design_request.request_id})
            Notification.objects.create(
                recipient=design_request.designer,
                message=f"Có một phản hồi từ Thư ký cho bản thiết kế '{product.name}'.",
                url=notification_url,
                is_read=False
            )
            logger.info(f"Notification created for designer {design_request.designer.username} for feedback on product {product.name}")

            messages.success(request, "Phản hồi đã được tạo thành công!")
            return redirect('secretary_feedback_list', request_id=request_id)
    else:
        form = RequestFeedbackForm()

    return render(request, 'myapp/secretary/feedback/create.html', {
        'form': form,
        'design_request': design_request,
    })

@role_required('Thư ký')
def secretary_products_feedback_list(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    feedbacks = ProductFeedback.objects.filter(product=product)
    
    return render(request, 'myapp/secretary/products/list_feedback.html', {
        'product': product,
        'feedbacks': feedbacks
    })

@role_required('Thư ký')
def secretary_update_status(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)
    new_status = request.POST.get('status')

    # Lấy đối tượng product ngay từ đầu để tránh lỗi UnboundLocalError
    product = design_request.product

    # Cập nhật trạng thái của yêu cầu thiết kế
    design_request.status = new_status
    design_request.save()

    # Logic thông báo tùy theo trạng thái
    if new_status == 'Chấp nhận':
        product = design_request.product
        product.description = design_request.description
        product.file_path = design_request.file_path
        product.status = 'Chờ phát hành'
        product.progress = 75  # Cập nhật tiến độ khi chuyển sang "Chờ phát hành"
        product.save()
        messages.success(request, 'Sản phẩm đã được chấp nhận, đang chờ được phát hành!')

        managers = CustomUser.objects.filter(role='Trưởng phòng')
        notification_url = reverse('manager_product_list')
        for manager in managers:
            Notification.objects.create(
                recipient=manager,
                message=f"Sản phẩm '{product.name}' đang chờ phát hành.",
                url=notification_url
            )
    elif new_status == 'Từ chối':
        # Khi Thư ký từ chối, chuyển trạng thái sản phẩm thành "Đã huỷ"
        product.status = 'Đã huỷ'
        product.progress = 0  # Đặt tiến độ về 0, giống như khi Trưởng phòng hủy
        product.save()
        messages.warning(request, 'Sản phẩm đã bị từ chối và quá trình thiết kế đã bị dừng!')

        # Gửi thông báo cho Người thiết kế
        designer = design_request.designer
        if designer:
            notification_url = reverse('designer_product_list')
            Notification.objects.create(
                recipient=designer,
                message=f"Sản phẩm '{product.name}' đã bị từ chối bởi Thư ký và quá trình thiết kế đã bị dừng.",
                url=notification_url,
                is_read=False
            )
            logger.info(f"Notification sent to designer {designer.username} for rejected product {product.name}")

    return redirect('secretary_design_request_list', product_id=product.product_id)


@role_required('Thư ký')
def secretary_designrequests_feedback_list(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)
    
    feedbacks = RequestFeedback.objects.filter(request=design_request)
    
    return render(request, 'myapp/secretary/feedback/list.html', {
        'design_request': design_request,
        'feedbacks': feedbacks
    })
    

# NGƯỜI THIẾT KẾ
@role_required('Người thiết kế')
def designer_product_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')  # Thêm tham số status_filter

    # Bắt đầu với tất cả sản phẩm
    products = Product.objects.all()

    # Lọc theo search_query nếu có
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Lọc theo status_filter nếu có
    if status_filter:
        products = products.filter(status=status_filter)

    unread_count = request.user.notifications.filter(is_read=False).count()
    notifications = request.user.notifications.all().order_by('-created_at')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = []
        for product in products:
            design_request = DesignRequest.objects.filter(product=product).first()
            products_data.append({
                'product_id': product.product_id,
                'name': product.name,
                'status': product.get_status_display(),
                'progress': product.progress,
                'created_at': product.created_at.strftime('%d/%m/%Y'),
                'file_path': design_request.file_path if design_request else None,
            })
        return JsonResponse({
            'products': products_data,
            'unread_count': unread_count,
        })

    context = {
        'current_page': 'product_list',
        'products': products,
        'search_query': search_query,
        'status_filter': status_filter,  # Thêm status_filter vào context để sử dụng trong template
        'unread_count': unread_count,
        'notifications': notifications,
    }
    return render(request, 'myapp/designer/products/list.html', context)


@role_required('Người thiết kế')
def designer_design_request_list(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    design_requests = DesignRequest.objects.filter(product=product)

    return render(request, 'myapp/designer/design/list.html', {
        'product': product,
        'design_requests': design_requests
    })
    

@role_required('Người thiết kế')
def designer_create_design_request(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if request.user.role != 'Người thiết kế':
        return HttpResponse("403 Forbidden", status=403)

    if request.method == "POST":
        form = DesignRequestForm(request.POST, request.FILES)
        form.instance.designer = request.user
        form.instance.product = product

        if form.is_valid():
            try:
                design_request = form.save(commit=False)
                
                if 'file' in request.FILES:
                    file = request.FILES['file']
                    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'design_requests'))
                    filename = fs.save(file.name, file)
                    design_request.file_path = os.path.join('design_requests', filename)
                
                design_request.save()
                # Tạo thông báo cho Thư ký
                notification_url = reverse('secretary_design_request_list', kwargs={'product_id': product.product_id})
                secretaries = CustomUser.objects.filter(role='Thư ký')  # Đảm bảo gửi cho tất cả Thư ký
                for secretary in secretaries:
                    Notification.objects.create(
                        recipient=secretary,
                        message=f"Đã nhận được bản thiết kế từ Người thiết kế cho sản phẩm '{product.name}'.",
                        url=notification_url,
                        is_read=False
                    )
                logger.info(f"Design request created for product {product_id} by {request.user.username}, notification sent to secretaries")
                messages.success(request, "Yêu cầu thiết kế đã được tạo thành công!")
                return redirect('designer_product_list')

            except Exception as e:
                logger.error(f"Error creating design request for product {product_id} by {request.user.username}: {e}")
                return HttpResponse("An error occurred while creating the design request.", status=500)
        else:
            logger.warning(f"Form for design request is invalid: {form.errors}")
            return HttpResponse("Form submission is invalid.", status=400)

    else:
        form = DesignRequestForm(initial={'designer': request.user})

    return render(request, 'myapp/designer/design/create.html', {
        'form': form,
        'product': product
    })



@role_required('Người thiết kế')
def designer_edit_design_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)

    if request.user != design_request.designer:
        logger.warning(f"Unauthorized access attempt by {request.user.username} to edit design request {request_id}")
        return HttpResponse("403 Forbidden", status=403)

    if request.method == "POST":
        form = DesignRequestForm(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            updated_design_request = form.save(commit=False)

            if 'file' in request.FILES:
                updated_design_request.file_path = request.FILES['file']

            updated_design_request.save()

            # Tạo thông báo cho Thư ký
            product = updated_design_request.product
            notification_url = reverse('secretary_design_request_list', kwargs={'product_id': product.product_id})
            secretaries = CustomUser.objects.filter(role='Thư ký')
            for secretary in secretaries:
                Notification.objects.create(
                    recipient=secretary,
                    message=f"Đã nhận được bản thiết kế từ Người thiết kế cho sản phẩm '{product.name}'.",
                    url=notification_url,
                    is_read=False
                )
            logger.info(f"Design request {request_id} updated by {request.user.username}, notification sent to secretaries")
            messages.success(request, "Yêu cầu thiết kế đã được cập nhật thành công!")
            return redirect('designer_product_list')

        else:
            logger.warning(f"Form for design request edit is invalid: {form.errors}")
            return HttpResponse("Form submission is invalid.", status=400)

    else:
        form = DesignRequestForm(instance=design_request)

    return render(request, 'myapp/designer/design/edit.html', {
        'form': form,
        'design_request': design_request
    })

@role_required('Người thiết kế')
def designer_delete_design_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)
    
    if request.user != design_request.designer:
        return HttpResponse("403 Forbidden", status=403)
    
    try:
        design_request.delete()
        logger.info(f"Design request {request_id} deleted successfully by {request.user.username}")
        return redirect('designer_product_list')  
    except Exception as e:
        logger.error(f"Error deleting design request {request_id} by {request.user.username}: {e}")
        return HttpResponse("An error occurred while deleting the design request.", status=500)
    
@role_required('Người thiết kế')
def designer_designrequests_feedback_list(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)
    
    feedbacks = RequestFeedback.objects.filter(request=design_request)
    
    return render(request, 'myapp/designer/feedback/list.html', {
        'design_request': design_request,
        'feedbacks': feedbacks
    })


#TRƯỞNG PHÒNG
@role_required('Trưởng phòng')
def manager_product_list(request):
    # Lấy giá trị tìm kiếm từ request.GET, mặc định là rỗng nếu không có
    search_query = request.GET.get('search', '')

    # Lọc sản phẩm dựa trên trạng thái 'Chờ phát hành' hoặc 'Đã phát hành' và tìm kiếm theo tên
    if search_query:
        products = Product.objects.filter(
            status__in=['Chờ phát hành', 'Đã phát hành'],
            name__icontains=search_query  # Tìm kiếm không phân biệt hoa thường
        )
    else:
        products = Product.objects.filter(
            status__in=['Chờ phát hành', 'Đã phát hành']  # Chỉ lấy sản phẩm chờ phát hành hoặc đã phát hành
        )

    unread_count = request.user.notifications.filter(is_read=False).count()

    notifications = request.user.notifications.all().order_by('-created_at')
    print(f"User: {request.user.username}, Notifications count: {notifications.count()}")

    # Kiểm tra nếu là yêu cầu AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = [
            {
                'product_id': product.product_id,
                'name': product.name,
                'file_path': product.file_path if product.file_path else None,
                'status': product.get_status_display(),
                'progress': product.progress,
                'created_at': product.created_at.strftime('%d/%m/%Y'),
            }
            for product in products
        ]
        return JsonResponse({
            'products': products_data,
            'unread_count': unread_count,
        })

    context = {
        'current_page': 'product_list',
        'products': products,
        'search_query': search_query,  # Truyền giá trị tìm kiếm để giữ trong input
        'unread_count': unread_count,
        'notifications': notifications,
    }
    return render(request, 'myapp/manager/products/list.html', context)

@role_required('Trưởng phòng')
def manager_update_status(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    new_status = request.POST.get('status')

    product.status = new_status
    if new_status == 'Đã phát hành':
        product.progress = 100  # Cập nhật tiến độ khi phát hành
    elif new_status == 'Đã huỷ':
        product.progress = 0  # Cập nhật tiến độ khi hủy
    product.save()

    messages.success(request, 'Sản phẩm đã được phát hành')

    # Tạo thông báo cho Thư ký (created_by)
    if new_status == 'Đã phát hành':
        notification_url = reverse('secretary_product_list')
        Notification.objects.create(
            recipient=product.created_by,
            message=f"Sản phẩm '{product.name}' đã được phát hành.",
            url=notification_url
        )

    return redirect('manager_product_list')

from django.shortcuts import render, get_object_or_404, redirect
from .forms import RequestFeedbackForm, ProductFeedbackForm
from .models import DesignRequest, RequestFeedback
from django.contrib.auth.decorators import login_required


@role_required('Trưởng phòng')
def manager_products_feedback_list(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    feedbacks = ProductFeedback.objects.filter(product=product)
    
    unread_count = request.user.notifications.filter(is_read=False).count()

    notifications = request.user.notifications.all().order_by('-created_at')
    print(f"User: {request.user.username}, Notifications count: {notifications.count()}")

    context = {
        'unread_count': unread_count,
        'notifications': notifications,
    }

    return render(request, 'myapp/manager/feedback/list.html', {
        'product': product,
        'feedbacks': feedbacks
    })

@role_required('Trưởng phòng')
def manager_create_feedback(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        form = ProductFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.product = product 
            feedback.sender = request.user    
            feedback.receiver = product.created_by  
            feedback.save()

            # Cập nhật trạng thái sản phẩm thành "Đang được thiết kế"
            product.status = 'Đang được thiết kế'
            product.progress = 25  # Cập nhật tiến độ khi chuyển về "Đang được thiết kế"
            product.save()

            # Tạo thông báo cho Thư ký
            notification_url = reverse('secretary_products_feedback_list', kwargs={'product_id': product.product_id})
            Notification.objects.create(
                recipient=product.created_by,
                message=f"Trưởng phòng đã gửi phản hồi cho sản phẩm '{product.name}'. Trạng thái đã chuyển về 'Đang được thiết kế'.",
                url=notification_url
            )
            
            return redirect('manager_products_feedback_list', product_id=product_id)
    else:
        form = ProductFeedbackForm()

    return render(request, 'myapp/manager/feedback/create.html', {
        'form': form,
        'product': product,
    })

def secretary_accept_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.status = 'Accepted'
    product.save()
    messages.success(request, 'Sản phẩm đã được chấp nhận!')
    return redirect('secretary_product_list')

def manager_release_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.status = 'Released'
    product.save()
    messages.success(request, 'Sản phẩm đã được phát hành!')
    return redirect('manager_product_list')


@login_required
def get_statistics(request):
    selected_date = request.GET.get('date')
    
    if selected_date:
        date = parse_date(selected_date)
        num_products_dang_thiet_ke = Product.objects.filter(status='Đang được thiết kế', created_at__date=date).count()
        num_products_dang_chua_phat_hanh = Product.objects.filter(status='Chờ phát hành', created_at__date=date).count()
        num_products_da_huy = Product.objects.filter(status='Đã huỷ', created_at__date=date).count()
        num_products_da_phat_hanh = Product.objects.filter(status='Đã phát hành', created_at__date=date).count()
    else:
        today = now()
        num_products_dang_thiet_ke = Product.objects.filter(status='Đang được thiết kế', created_at__year=today.year, created_at__month=today.month).count()
        num_products_dang_chua_phat_hanh = Product.objects.filter(status='Chờ phát hành', created_at__year=today.year, created_at__month=today.month).count()
        num_products_da_huy = Product.objects.filter(status='Đã huỷ', created_at__year=today.year, created_at__month=today.month).count()
        num_products_da_phat_hanh = Product.objects.filter(status='Đã phát hành', created_at__year=today.year, created_at__month=today.month).count()

    context = {
        'num_products_dang_thiet_ke': num_products_dang_thiet_ke,
        'num_products_dang_chua_phat_hanh': num_products_dang_chua_phat_hanh,
        'num_products_da_huy': num_products_da_huy,
        'num_products_da_phat_hanh': num_products_da_phat_hanh,
    }
    return JsonResponse(context)

@login_required
def notifications_list(request):
    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        if not notification_id:
            return JsonResponse({'status': 'error', 'message': 'Notification ID is required'}, status=400)

        try:
            # Sửa 'id' thành 'notification_id'
            notification = get_object_or_404(Notification, notification_id=notification_id, recipient=request.user)
            notification.is_read = True
            notification.save()

            # Tùy chọn: Trả về số lượng thông báo chưa đọc còn lại
            unread_count = request.user.notifications.filter(is_read=False).count()
            return JsonResponse({'status': 'success', 'unread_count': unread_count})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
import json

@login_required
@csrf_exempt
def send_chat_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        if message:
            ChatMessage.objects.create(sender=request.user, content=message, is_read=False)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def get_chat_messages(request):
    messages = ChatMessage.objects.all().order_by('-timestamp')[:50][::-1]
    return JsonResponse({
        'messages': [
            {
                'sender': msg.sender.username,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M')
            } for msg in messages
        ]
    })


# views.py
@login_required
@csrf_exempt
def mark_chat_as_read(request):
    if request.method == 'POST':
        ChatMessage.objects.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
@csrf_exempt
def mark_notification_as_read(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, notification_id=notification_id, recipient=request.user)
        if not notification.is_read:
            notification.is_read = True
            notification.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def mark_notification_as_read(request, notification_id):
    # Lấy thông báo theo ID và đảm bảo nó thuộc về người dùng hiện tại
    notification = get_object_or_404(Notification, notification_id=notification_id, recipient=request.user)
    
    # Đánh dấu thông báo là đã đọc
    if not notification.is_read:
        notification.is_read = True
        notification.save()
        logger.info(f"Notification {notification_id} marked as read by {request.user.username}")
    
    # Chuyển hướng đến URL được lưu trong thông báo
    return redirect(notification.url)