from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from django.contrib.auth.decorators import login_required, user_passes_test
import subprocess
from django.db import connections
from django.db.utils import OperationalError
from django.utils import timezone
from .models import Visit

def health_check(request):
    return JsonResponse({'status': 'ok'})

def get_git_revision_hash():
    try:
        # Get the latest git commit hash
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 'N/A'

@login_required
@user_passes_test(lambda u: u.is_superuser)
def status_view(request):
    # Check database connection
    db_conn = connections['default']
    try:
        db_conn.cursor()
        db_status = 'ok'
    except OperationalError:
        db_status = 'error'

    # Stats
    today = timezone.now().date()
    visits_today = Visit.objects.filter(timestamp__date=today).count()
    visits_total = Visit.objects.count()
    latest_visits = Visit.objects.all()[:10]

    context = {
        'db_status': db_status,
        'debug_mode': settings.DEBUG,
        'git_commit': get_git_revision_hash(),
        'visits_today': visits_today,
        'visits_total': visits_total,
        'latest_visits': latest_visits,
    }
    return render(request, 'status.html', context)


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def process(request):
    return render(request, 'process.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get cleaned data
            name = form.cleaned_data['name']
            contact_person = form.cleaned_data.get('contact_person', '-')
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', '-')
            message = form.cleaned_data['message']

            # Construct email
            subject = f"Neue Anfrage von {name}"
            email_message = f"""
            Neue Kontaktanfrage über die Website:

            Firma/Name: {name}
            Ansprechpartner: {contact_person}
            E-Mail: {email}
            Telefon: {phone}

            Nachricht:
            {message}
            """
            
            try:
                # Send email
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['kontakt@suedwest-energie.de'],
                    fail_silently=False,
                )
                messages.success(request, 'Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns umgehend bei Ihnen.')
                return redirect('contact')
            except Exception as e:
                messages.error(request, 'Es gab einen Fehler beim Senden Ihrer Nachricht. Bitte versuchen Sie es später erneut oder rufen Sie uns an.')
                # In production, log the error here
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def imprint(request):
    return render(request, 'home.html') # Placeholder, reusing home for now

def privacy(request):
    return render(request, 'home.html') # Placeholder, reusing home for now

def terms(request):
    return render(request, 'home.html') # Placeholder, reusing home for now