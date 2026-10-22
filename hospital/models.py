"""医院业务系统 —— 数据模型。

实体关系:
Department(科室) 1 ── * Doctor(医生)
Patient(患者)    1 ── * Registration(挂号)
Doctor           1 ── * Registration
Registration     1 ── 1 MedicalRecord(就诊记录/病历)
"""
from django.db import models
from django.utils import timezone


class Department(models.Model):
    """科室。"""
    name = models.CharField('科室名称', max_length=50, unique=True)
    description = models.CharField('简介', max_length=200, blank=True)

    class Meta:
        verbose_name = '科室'
        verbose_name_plural = '科室'
        ordering = ['id']

    def __str__(self):
        return self.name


class Doctor(models.Model):
    """医生。"""
    TITLES = [
        ('主任医师', '主任医师'),
        ('副主任医师', '副主任医师'),
        ('主治医师', '主治医师'),
        ('住院医师', '住院医师'),
    ]
    name = models.CharField('姓名', max_length=30)
    title = models.CharField('职称', max_length=20, choices=TITLES, default='主治医师')
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='doctors', verbose_name='科室')
    specialty = models.CharField('专长', max_length=100, blank=True)
    is_active = models.BooleanField('在岗', default=True)

    class Meta:
        verbose_name = '医生'
        verbose_name_plural = '医生'
        ordering = ['department__id', 'id']

    def __str__(self):
        return f'{self.name}({self.get_title_display()})'


class Patient(models.Model):
    """患者。"""
    GENDERS = [('男', '男'), ('女', '女')]
    name = models.CharField('姓名', max_length=30)
    gender = models.CharField('性别', max_length=4, choices=GENDERS, default='男')
    birth_date = models.DateField('出生日期', null=True, blank=True)
    phone = models.CharField('联系电话', max_length=20, blank=True)
    address = models.CharField('住址', max_length=200, blank=True)
    created_at = models.DateTimeField('建档时间', auto_now_add=True)

    class Meta:
        verbose_name = '患者'
        verbose_name_plural = '患者'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = timezone.localdate()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class Registration(models.Model):
    """挂号/预约记录。"""
    STATUS = [
        ('waiting', '待就诊'),
        ('done', '已就诊'),
        ('cancelled', '已取消'),
    ]
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='registrations', verbose_name='患者')
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='registrations', verbose_name='科室')
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='registrations', verbose_name='医生')
    visit_date = models.DateField('就诊日期', default=timezone.localdate)
    status = models.CharField('状态', max_length=10, choices=STATUS, default='waiting')
    fee = models.DecimalField('挂号费', max_digits=8, decimal_places=2, default=10.00)
    created_at = models.DateTimeField('挂号时间', auto_now_add=True)

    class Meta:
        verbose_name = '挂号记录'
        verbose_name_plural = '挂号记录'
        ordering = ['-visit_date', '-created_at']

    def __str__(self):
        return f'{self.patient.name} · {self.doctor.name} · {self.visit_date}'


class MedicalRecord(models.Model):
    """就诊记录/病历(一次挂号对应一份)。"""
    registration = models.OneToOneField(
        Registration, on_delete=models.CASCADE, related_name='record', verbose_name='挂号')
    chief_complaint = models.CharField('主诉', max_length=200, blank=True)
    diagnosis = models.CharField('诊断', max_length=200, blank=True)
    prescription = models.TextField('处方/医嘱', blank=True)
    note = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('记录时间', auto_now_add=True)

    class Meta:
        verbose_name = '就诊记录'
        verbose_name_plural = '就诊记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.registration.patient.name} · {self.diagnosis or "未诊断"}'
