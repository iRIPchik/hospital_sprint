from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Appointment, ScheduleSlot


class AppointmentCreateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "slot"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.fields["slot"].queryset = (
            ScheduleSlot.objects.filter(
                appointment__isnull=True, start_time__gte=now
            )
            .select_related("doctor")
            .order_by("start_time")
        )

    def clean_slot(self):
        slot = self.cleaned_data.get("slot")
        if not slot:
            return slot

        # Ensure slot is future
        if slot.start_time < timezone.now():
            raise ValidationError("Выбраный слот уже в прошлом.")

        # Ensure slot is free
        if hasattr(slot, "appointment"):
            raise ValidationError("Слот уже занят.")

        return slot

    def _slot_label(self, slot: ScheduleSlot) -> str:
        dt = timezone.localtime(slot.start_time)
        return (
            f"{slot.doctor.full_name} | {slot.doctor.specialty} | "
            f"{slot.doctor.cabinet} | {dt.strftime('%Y-%m-%d %H:%M')}"
        )

    def label_from_instance(self, obj):
        # Used by ModelChoiceField to render each option label
        if isinstance(obj, ScheduleSlot):
            return self._slot_label(obj)
        return super().label_from_instance(obj)


class DoctorFilterForm(forms.Form):
    specialty = forms.CharField(required=False)
