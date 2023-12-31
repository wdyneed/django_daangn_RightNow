from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    signup_date = models.DateTimeField(default=timezone.now)  # Add signup date field

    location = models.CharField(max_length=100, default=None, null=True)
    location_certified = models.BooleanField(default=False)
    user_img = models.ImageField(upload_to="user_img", default=None, null=True)
    nickname = models.CharField(max_length=50, default=" ")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="글 제목")
    price = models.IntegerField(verbose_name="가격")
    description = models.TextField(verbose_name="설명")
    category = models.CharField(max_length=255)
    view_count = models.PositiveIntegerField(default=0, verbose_name="조회수")
    created_at = models.DateTimeField(verbose_name="업로드 날짜", auto_now_add=True)
    updated = models.CharField(verbose_name="끌올", default="N")
    wt_location = models.CharField(max_length=300, verbose_name="판매 원하는 장소")
    status = models.CharField(max_length=100, default="판매중", verbose_name="판매 상태")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="작성자", default="NONE"
    )
    chat_num = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0, verbose_name="관심 수")


class chatroom(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    chatroom_id = models.ForeignKey(chatroom, on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    send_at = models.DateTimeField(auto_now_add=True)
    chat_img = models.ImageField(upload_to="chat")

class ai_chatroom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ai = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class ai_ChatMessage(models.Model):
    chatroom_id = models.ForeignKey(ai_chatroom, on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.PositiveIntegerField()
    send_at = models.DateTimeField(auto_now_add=True)
        
    
    
# 이미지 업로드 경로
def image_upload_path(instance, filename):
    return f"{instance.post.id}/{filename}"


# 다중 이미지 업로드를 위한 테이블
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to="image_upload_path/", blank=True)

    def __int__(self):
        return self.id

# 웹 소켓 disconnect 저장 테이블
class DisconnectInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자와 연결
    chat_room = models.ForeignKey(chatroom, on_delete=models.CASCADE, null=True)  # 나갔던 채팅방의 ID
    disconnect_time = models.DateTimeField()  # 나갔던 시간