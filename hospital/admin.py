from django.contrib import admin
from .models import (Department, Doctor, Patient, Registration, MedicalRecord)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'department', 'specialty', 'is_active')
    list_filter = ('department', 'title', 'is_active')
    search_fields = ('name',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birth_date', 'phone', 'created_at')
    search_fields = ('name', 'phone')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'department', 'doctor', 'visit_date', 'status', 'fee')
    list_filter = ('status', 'department', 'visit_date')
    search_fields = ('patient__name',)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('registration', 'chief_complaint', 'diagnosis', 'created_at')
    search_fields = ('registration__patient__name', 'diagnosis')
