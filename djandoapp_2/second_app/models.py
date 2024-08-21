from django.db import models

class UserProfile(models.Model):
    # ユーザーの名前
    username = models.CharField(max_length=150, unique=True)
    
    # メールアドレス
    email = models.EmailField(unique=True)
    
    # プロフィール画像
    # profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    #パスワード
    password=models.CharField(max_length=20)

    # 文字列表現
    def __str__(self):
        return self.username


# Create your models here.
