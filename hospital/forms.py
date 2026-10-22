"""医院业务系统 —— 表单。"""
from django import forms
from .models import Department, Doctor, Patient, Registration, MedicalRecord


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'title', 'department', 'specialty', 'is_active']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'gender', 'birth_date', 'phone', 'address']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['patient', 'department', 'doctor', 'visit_date', 'fee']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 医生下拉框同时展示所属科室,便于选择
        self.fields['doctor'].queryset = Doctor.objects.filter(
            is_active=True).select_related('department')
        self.fields['doctor'].label_from_instance = (
            lambda d: f'{d.name}（{d.department.name}·{d.get_title_display()}）')


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['registration', 'chief_complaint', 'diagnosis', 'prescription', 'note']
        widgets = {
            'chief_complaint': forms.TextInput(attrs={'placeholder': '例：发热咳嗽 3 天'}),
            'diagnosis': forms.TextInput(attrs={'placeholder': '例：上呼吸道感染'}),
            'prescription': forms.Textarea(attrs={'rows': 3, 'placeholder': '例：阿莫西林 0.5g 每日 3 次'}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只允许为尚未建病历的挂号创建记录
        self.fields['registration'].queryset = Registration.objects.filter(
            record__isnull=True).exclude(status='cancelled').select_related('patient', 'doctor')
        self.fields['registration'].label_from_instance = (
            lambda r: f'{r.patient.name} · {r.doctor.name} · {r.visit_date}')
