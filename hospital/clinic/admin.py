from django.contrib import admin

from .models import Appointment, Doctor, Patient, ScheduleSlot


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialty", "cabinet", "is_active")
    list_filter = ("specialty", "is_active")
    search_fields = ("full_name", "specialty", "cabinet")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "birth_date", "attached_since")
    search_fields = ("full_name", "phone")


@admin.register(ScheduleSlot)
class ScheduleSlotAdmin(admin.ModelAdmin):
    list_display = ("doctor", "start_time", "end_time", "is_free")
    list_filter = ("doctor", "start_time")
    search_fields = (
        "doctor__full_name",
        "doctor__specialty",
        "doctor__cabinet",
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "slot", "created_at")
    list_filter = ("created_at", "slot__doctor")
    search_fields = ("patient__full_name", "slot__doctor__full_name")
