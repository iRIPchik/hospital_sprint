from django.db import models


class Doctor(models.Model):
	full_name = models.CharField(max_length=255)
	specialty = models.CharField(max_length=120)
	cabinet = models.CharField(max_length=20)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.full_name} ({self.specialty})"


class Patient(models.Model):
	full_name = models.CharField(max_length=255)
	phone = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	attached_since = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.full_name


class ScheduleSlot(models.Model):
	doctor = models.ForeignKey(
		'Doctor', related_name='slots', on_delete=models.CASCADE
	)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	class Meta:
		ordering = ['start_time']

	def __str__(self):
		return f"{self.doctor.full_name}: {self.start_time} - {self.end_time}"

	@property
	def is_free(self) -> bool:
		return not hasattr(self, 'appointment')


class Appointment(models.Model):
	patient = models.ForeignKey(
		'Patient', related_name='appointments', on_delete=models.CASCADE
	)
	slot = models.OneToOneField(
		'ScheduleSlot', related_name='appointment', on_delete=models.CASCADE
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.patient.full_name} @ {self.slot.start_time}"
