from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm

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