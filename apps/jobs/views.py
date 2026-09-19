from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from .models import JobListing
from .forms import JobApplicationForm

def job_list(request):
    jobs = JobListing.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'careers/job_list.html', {'jobs': jobs})

def job_apply(request, pk):
    """Page 2: Dedicated Job Application Form."""
    job = get_object_or_404(JobListing, pk=pk, is_active=True)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            cv_file = request.FILES['cv']

            email_body = f"""
            New Application Received for {job.title}:

            Name: {data['first_name']} {data['last_name']}
            Email: {data['email']}
            Phone: {data['phone']}

            Cover Letter:
            {data['cover_letter']}
            """

            msg = EmailMessage(
                subject=f"Job Application: {job.title} - {data['first_name']} {data['last_name']}",
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['hr@yourdomain.com'],
                reply_to=[data['email']]
            )
            msg.attach(cv_file.name, cv_file.read(), cv_file.content_type)
            msg.send()

            # Return partial HTMX snippet on HTMX request
            if request.headers.get('HX-Request'):
                return render(request, 'careers/application_success.html', {'job': job})

            return render(request, 'careers/job_apply_success.html', {'job': job})
        
        # Form is invalid: return form partial with validation errors for HTMX
        if request.headers.get('HX-Request'):
            return render(request, 'careers/application_form_wrapper.html', {'job': job, 'form': form})
    else:
        form = JobApplicationForm()

    return render(request, 'careers/job_apply.html', {'job': job, 'form': form})