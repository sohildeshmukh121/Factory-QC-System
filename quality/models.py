
from django.db import models
from django.core.validators import MinValueValidator


class ProductionJob(models.Model):
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
    ]

    part_number = models.CharField(
        max_length=50,
        unique=True
    )

    part_name = models.CharField(
        max_length=100
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.part_number} - {self.part_name}"


class QualityInspection(models.Model):
    RESULT_CHOICES = [
        ('PASS', 'Pass'),
        ('FAIL', 'Fail'),
    ]

    APPROVAL_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    job = models.ForeignKey(
        ProductionJob,
        on_delete=models.CASCADE,
        related_name='inspections'
    )

    actual_measurement = models.FloatField()
    min_tolerance = models.FloatField()
    max_tolerance = models.FloatField()

    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES,
        editable=False
    )

    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='PENDING'
    )

    is_final = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)

    inspected_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if self.min_tolerance > self.max_tolerance:
            raise ValueError(
                "Minimum tolerance cannot exceed maximum tolerance."
            )

        if self.min_tolerance <= self.actual_measurement <= self.max_tolerance:
            self.result = 'PASS'
        else:
            self.result = 'FAIL'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job.part_number} - {self.result}"
