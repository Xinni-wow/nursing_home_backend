from django.db import models
from elders.models import Elder
from django.utils import timezone

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(default=1)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_number}（{'已占用' if self.is_occupied else '可用'}）"

class CheckIn(models.Model):
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE, verbose_name="入住老人")  # ✅ 保持字段名为 elder
    room = models.ForeignKey(Room, on_delete=models.PROTECT, verbose_name="房间")

    start_date = models.DateField(verbose_name="入住日期")
    duration_years = models.PositiveIntegerField(default=1, verbose_name="入住年限（年）")

    checkin_date = models.DateField(auto_now_add=True, verbose_name="提交日期")

    STATUS_CHOICES = (
        ('active', '在住'),
        ('left', '已退房'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="入住状态")

    class Meta:
        verbose_name = "入住记录"
        verbose_name_plural = "入住记录"

    def __str__(self):
        return f"{self.elder.full_name} 入住 {self.room.room_number}"

    def save(self, *args, **kwargs):
        self.stay_fee = self.duration_years * 8000
        self.meal_fee = self.duration_years * 5000
        self.total_fee = self.stay_fee + self.meal_fee

        self.room.is_occupied = True
        self.room.save()
        super().save(*args, **kwargs)


class Bill(models.Model):
    BILL_TYPE_CHOICES = (
        ('initial', '首次入住'),
        ('renew', '续费'),
    )

    checkin = models.ForeignKey(CheckIn, on_delete=models.CASCADE, related_name='bills')
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE)
    years = models.PositiveIntegerField()

    stay_fee = models.DecimalField(max_digits=10, decimal_places=2)
    meal_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)

    type = models.CharField(max_length=10, choices=BILL_TYPE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.elder.full_name} - ￥{self.total_fee} - {self.get_type_display()}"