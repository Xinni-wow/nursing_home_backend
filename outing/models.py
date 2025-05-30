from django.db import models
from accounts.models import CustomUser
from elders.models import Elder  # 假设 Elder 在 elder app 下

class OutingRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="用户")  # 直接关联用户
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE, null=True, blank=True, verbose_name="老人")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    reason = models.TextField(verbose_name="外出事由")

    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('canceled', '用户已撤销'),
        ('approved', '审批通过'),
        ('rejected', '审批拒绝'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="申请状态")

    remarks = models.TextField(null=True, blank=True, verbose_name="备注")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        elder_name = self.elder.full_name if self.elder else "未知老人"
        return f"{elder_name} 的外出申请 ({self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%Y-%m-%d %H:%M')}) 状态：{self.get_status_display()}"
