
from django.contrib import admin
from .models import ProductionJob, QualityInspection


@admin.register(ProductionJob)
class ProductionJobAdmin(admin.ModelAdmin):
    list_display = (
        'part_number',
        'part_name',
        'quantity',
        'status',
        'created_at',
    )

    list_filter = ('status', 'created_at')
    search_fields = ('part_number', 'part_name')
    list_editable = ('status',)
    ordering = ('-created_at',)


@admin.register(QualityInspection)
class QualityInspectionAdmin(admin.ModelAdmin):
    list_display = (
        'job',
        'actual_measurement',
        'min_tolerance',
        'max_tolerance',
        'result',
        'approval_status',
        'is_final',
        'inspected_at',
    )

    list_filter = ('result', 'approval_status', 'is_final')
    search_fields = ('job__part_number', 'job__part_name')
