"""医院业务系统 —— 视图(函数视图)。"""
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Department, Doctor, Patient, Registration, MedicalRecord
from .forms import (DepartmentForm, DoctorForm, PatientForm,
                    RegistrationForm, MedicalRecordForm)


def index(request):
    """总览仪表盘。"""
    today = timezone.localdate()
    ctx = {
        'n_departments': Department.objects.count(),
        'n_doctors': Doctor.objects.filter(is_active=True).count(),
        'n_patients': Patient.objects.count(),
        'n_registrations': Registration.objects.count(),
        'n_today': Registration.objects.filter(visit_date=today).count(),
        'n_waiting': Registration.objects.filter(status='waiting').count(),
        'n_done': Registration.objects.filter(status='done').count(),
        'n_records': MedicalRecord.objects.count(),
        'recent_regs': Registration.objects.select_related(
            'patient', 'doctor', 'department').order_by('-created_at')[:8],
    }
    return render(request, 'hospital/index.html', ctx)


def departments(request):
    """科室列表 + 新增科室表单。"""
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '科室已添加')
        return redirect('hospital:departments')
    deps = Department.objects.prefetch_related('doctors').all()
    ctx = {'departments': deps, 'form': form}
    return render(request, 'hospital/departments.html', ctx)


def doctors(request):
    """医生列表 + 新增医生表单。"""
    form = DoctorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '医生已添加')
        return redirect('hospital:doctors')
    docs = Doctor.objects.select_related('department').all()
    ctx = {'doctors': docs, 'form': form}
    return render(request, 'hospital/doctors.html', ctx)


def patients(request):
    """患者列表 + 新增患者表单。"""
    form = PatientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '患者已建档')
        return redirect('hospital:patients')
    pts = Patient.objects.all()
    ctx = {'patients': pts, 'form': form}
    return render(request, 'hospital/patients.html', ctx)


def registrations(request):
    """挂号列表 + 新增挂号表单。"""
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '挂号成功')
        return redirect('hospital:registrations')
    regs = Registration.objects.select_related(
        'patient', 'doctor', 'department').all()
    ctx = {'regs': regs, 'form': form}
    return render(request, 'hospital/registrations.html', ctx)


def registration_action(request, pk):
    """挂号状态变更(done / cancel)。"""
    reg = get_object_or_404(Registration, pk=pk)
    action = request.POST.get('action')
    if action == 'done':
        reg.status = 'done'
        reg.save()
        messages.success(request, f'{reg.patient.name} 已标记为已就诊')
    elif action == 'cancel':
        reg.status = 'cancelled'
        reg.save()
        messages.success(request, f'{reg.patient.name} 的挂号已取消')
    return redirect('hospital:registrations')


def records(request):
    """就诊记录列表 + 新增就诊记录表单。"""
    form = MedicalRecordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        rec = form.save()
        # 建病历后自动把对应挂号置为已就诊
        reg = rec.registration
        reg.status = 'done'
        reg.save(update_fields=['status'])
        messages.success(request, '就诊记录已保存')
        return redirect('hospital:records')
    recs = MedicalRecord.objects.select_related(
        'registration__patient', 'registration__doctor').all()
    ctx = {'records': recs, 'form': form}
    return render(request, 'hospital/records.html', ctx)
