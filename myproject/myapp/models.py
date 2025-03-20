from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role=None):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, role=role)
        user.password = password  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, role='Trưởng phòng'):
        user = self.create_user(username, password, role)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    ROLE_CHOICES = [
        ('Thư ký', 'Thư ký'),
        ('Người thiết kế', 'Người thiết kế'),
        ('Trưởng phòng', 'Trưởng phòng')
    ]
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Thư ký')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.username

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    STATUS_CHOICES = [
        ('Đang được thiết kế', 'Đang được thiết kế'),
        ('Chờ phát hành', 'Chờ phát hành'),
        ('Đã phát hành', 'Đã phát hành'),
        ('Đã huỷ', 'Đã huỷ'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Đang được thiết kế')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.TextField(null=True, blank=True)
    designer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='designed_products')
    # Thêm trường progress
    progress = models.IntegerField(default=0)  # Phần trăm tiến độ (0-100)

    def __str__(self):
        return self.name

class DesignRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    designer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='designer_requests')
    description = models.TextField()
    STATUS_CHOICES = [
        ('Chấp nhận', 'Chấp nhận'),
        ('Từ chối', 'Từ chối'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Chờ chấp nhận')
    created_at = models.DateTimeField(auto_now_add=True)
    
    file_path = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Request for {self.product.name}"


class RequestFeedback(models.Model):
    request_feedback_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(DesignRequest, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_request_feedbacks')  # Changed related_name
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_request_feedbacks')  # Changed related_name
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.sender.username} to {self.receiver.username}"


class ProductFeedback(models.Model):
    product_feedback_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_product_feedbacks')  # Changed related_name
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_product_feedbacks')  # Changed related_name
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.sender.username} to {self.receiver.username}"

# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# (Các model hiện tại giữ nguyên)

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    url = models.URLField(max_length=200, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.message[:20]}"
    

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Thêm dòng này

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
