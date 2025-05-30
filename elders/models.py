from django.db import models
from accounts.models import CustomUser

class Elder(models.Model):
    GENDER_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )
    RELATIONSHIP_CHOICES = (
        ('父女', '父女'),
        ('母女', '母女'),
        ('父子', '父子'),
        ('母子', '母子'),
        ('配偶', '配偶'),
        ('本人', '本人'),
        ('其他', '其他'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='elders')
    photo = models.ImageField(upload_to='elder_photos/', null=True, blank=True)
    full_name = models.CharField(max_length=50)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='other',
                                    verbose_name="亲属关系")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    id_number = models.CharField(max_length=18, unique=True,        error_messages={
            'unique': '该身份证号码已存在，请输入其他号码',
        })
    health_status = models.TextField()
    notes = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
