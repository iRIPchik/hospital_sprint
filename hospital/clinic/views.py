from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Doctor, ScheduleSlot
from .forms import AppointmentCreateForm


def doctors_list(request):
	specialty = request.GET.get("specialty")
	doctors = Doctor.objects.filter(is_active=True).order_by("full_name")
	if specialty:
		doctors = doctors.filter(specialty__iexact=specialty)
	context = {"doctors": doctors, "specialty": specialty}
	return render(request, "clinic/doctors_list.html", context)


def doctor_schedule(request, doctor_id: int):
	doctor = get_object_or_404(Doctor, pk=doctor_id, is_active=True)
	now = timezone.now()
	slots = (
		ScheduleSlot.objects.filter(doctor=doctor, start_time__gte=now)
		.select_related("doctor")
		.order_by("start_time")
	)
	context = {"doctor": doctor, "slots": slots}
	return render(request, "clinic/doctor_schedule.html", context)


def appointment_create(request):
	initial = {}
	slot_error = None

	# Handle slot_id from GET
	slot_id = request.GET.get("slot_id")
	if slot_id:
		try:
			slot = ScheduleSlot.objects.select_related("doctor").get(pk=slot_id)
			# Validate slot is future and free
			now = timezone.now()
			if slot.start_time < now:
				slot_error = "Выбранный слот уже в прошлом."
			elif hasattr(slot, "appointment"):
				slot_error = "Выбранный слот уже занят."
			else:
				initial["slot"] = slot
		except ScheduleSlot.DoesNotExist:
			slot_error = "Слот не найден."

	if request.method == "POST":
		form = AppointmentCreateForm(request.POST)
		if form.is_valid():
			appointment = form.save()
			return redirect("clinic:doctor_schedule", doctor_id=appointment.slot.doctor_id)
	else:
		form = AppointmentCreateForm(initial=initial)
		if slot_error:
			form.add_error("slot", slot_error)

	return render(request, "clinic/appointment_form.html", {"form": form})
