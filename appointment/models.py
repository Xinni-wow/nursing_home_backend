from django.db import models
from accounts.models import CustomUser
from elders.models import Elder
import uuid
from datetime import datetime, timedelta


class VisitRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="申请人")
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE, verbose_name="拜访老人")
    visit_date = models.DateField(verbose_name="拜访日期")
    visit_time = models.TimeField(verbose_name="拜访时间")
    visitor_count = models.PositiveSmallIntegerField(default=1, verbose_name="来访人数")
    reason = models.TextField(verbose_name="来访事由")

    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('canceled', '已取消'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")

    # 二维码相关字段
    qr_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="二维码标识")
    qr_code_expiry = models.DateTimeField(blank=True, null=True, verbose_name="二维码有效期")

    remarks = models.TextField(blank=True, null=True, verbose_name="管理员备注")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return f"{self.elder.full_name}的来访预约({self.visit_date} {self.visit_time})"

    def save(self, *args, **kwargs):
        # 如果是新创建的记录且状态为approved，生成二维码
        if not self.pk and self.status == 'approved':
            self.generate_qrcode()
        super().save(*args, **kwargs)

    def generate_qrcode(self):
        """生成二维码标识和有效期"""
        self.qr_code = f"VISIT-{uuid.uuid4().hex[:8]}"
        self.qr_code_expiry = datetime.now() + timedelta(days=1)

    class Meta:
        verbose_name = "来访预约"
        verbose_name_plural = "来访预约"