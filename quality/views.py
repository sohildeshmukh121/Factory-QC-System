
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductionJob, QualityInspection
from .forms import ProductionJobForm, QualityInspectionForm


def dashboard(request):
    jobs = ProductionJob.objects.all().order_by('-created_at')
    inspections = QualityInspection.objects.all()

    context = {
        'total_jobs': jobs.count(),
        'active_jobs': jobs.filter(status='IN_PROGRESS').count(),
        'completed_jobs': jobs.filter(status='COMPLETED').count(),
        'total_inspections': inspections.count(),
        'passed_inspections': inspections.filter(result='PASS').count(),
        'failed_inspections': inspections.filter(result='FAIL').count(),
        'pending_inspections': inspections.filter(
            approval_status='PENDING'
        ).count(),
        'recent_jobs': jobs[:5],
    }

    return render(request, 'quality/dashboard.html', context)


def job_list(request):
    jobs = ProductionJob.objects.all().order_by('-created_at')
    return render(request, 'quality/job_list.html', {'jobs': jobs})


def create_job(request):
    if request.method == 'POST':
        form = ProductionJobForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Production job created successfully.'
            )
            return redirect('job_list')
    else:
        form = ProductionJobForm()

    return render(request, 'quality/job_form.html', {'form': form})


def inspection_list(request):
    inspections = QualityInspection.objects.select_related(
        'job'
    ).order_by('-inspected_at')

    return render(
        request,
        'quality/inspection_list.html',
        {'inspections': inspections}
    )


def create_inspection(request):
    if request.method == 'POST':
        form = QualityInspectionForm(request.POST)

        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.approval_status = 'PENDING'
            inspection.save()

            messages.success(
                request,
                f'Inspection recorded: {inspection.result}'
            )
            return redirect('inspection_list')
    else:
        form = QualityInspectionForm()

    return render(
        request,
        'quality/inspection_form.html',
        {'form': form}
    )


@login_required
def review_inspection(request, inspection_id, decision):
    inspection = get_object_or_404(
        QualityInspection,
        pk=inspection_id
    )

    if request.method != 'POST':
        messages.error(
            request,
            'Use the review button to submit a decision.'
        )
        return redirect('inspection_list')

    if decision == 'approve':
        if inspection.result != 'PASS':
            messages.error(
                request,
                'A failed inspection cannot be approved.'
            )
        else:
            inspection.approval_status = 'APPROVED'
            inspection.save()
            messages.success(request, 'Inspection approved.')

    elif decision == 'reject':
        inspection.approval_status = 'REJECTED'
        inspection.save()
        messages.warning(request, 'Inspection rejected.')

    else:
        messages.error(request, 'Invalid review decision.')

    return redirect('inspection_list')


def dispatch_clearance(request):
    jobs = ProductionJob.objects.all().order_by('-created_at')
    dispatch_rows = []

    for job in jobs:
        inspections = job.inspections.all()

        final_approved = inspections.filter(
            is_final=True,
            result='PASS',
            approval_status='APPROVED'
        ).exists()

        all_approved = (
            inspections.exists()
            and not inspections.exclude(
                result='PASS',
                approval_status='APPROVED'
            ).exists()
        )

        cleared = (
            job.status == 'COMPLETED'
            and final_approved
            and all_approved
        )

        dispatch_rows.append({
            'job': job,
            'cleared': cleared,
            'final_approved': final_approved,
            'all_approved': all_approved,
        })

    return render(
        request,
        'quality/dispatch.html',
        {'dispatch_rows': dispatch_rows}
    )
