import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from . import content
from .forms import ContactForm
from .models import Project

logger = logging.getLogger(__name__)


# Hosting platforms recognised from project links (shown in the gallery console).
_HOSTS = (("onrender.com", "Render"), ("vercel.app", "Vercel"), ("github.io", "GitHub Pages"))


def _console_data(projects):
    hosts = [label for domain, label in _HOSTS if any(domain in (p.link or "") for p in projects)]
    return {"count": len(projects), "titles": [p.title for p in projects], "hosts": hosts}


def _landing(request, form=None, scroll_to=""):
    projects = list(Project.objects.all())
    context = content.landing_context()
    context.update({
        "projects": projects,
        "console_data": _console_data(projects),
        "form": form or ContactForm(),
        "scroll_to": scroll_to,
    })
    return render(request, "main/index.html", context)


def _section(name):
    return redirect(f"{reverse('home')}#{name}")


# Home: the whole portfolio is one page with anchored sections.
def home(request):
    return _landing(request)


# The old multi-page URLs still work and jump to the matching section.
def about(request):
    return _section("about")


def projects(request):
    return _section("projects")


# Contact form endpoint (the form lives in the #contact section of the home page).
def contact(request):
    if request.method != "POST":
        return _section("contact")

    form = ContactForm(request.POST)
    if not form.is_valid():
        return _landing(request, form=form, scroll_to="contact")

    if form.cleaned_data["website"]:          # honeypot filled in -> bot; pretend it worked
        messages.success(request, "Your message has been sent successfully!")
        return _section("contact")

    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    message = form.cleaned_data["message"]

    # 1. Message to Anitha
    try:
        EmailMessage(
            subject=f"New Contact Form Submission from {name}",
            body=f"Message:\n{message}\n\nFrom: {name} ({email})",
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email],
        ).send(fail_silently=False)
    except Exception:
        logger.exception("Contact form: could not send message to owner")
        messages.error(
            request,
            "Sorry, your message could not be sent right now. "
            "Please email me directly or try again later.",
        )
        return _landing(request, form=form, scroll_to="contact")

    # 2. Acknowledgement to the visitor (a failure here should not lose the message)
    try:
        text_body = (
            f"Hi {name},\n\n"
            "Thank you for reaching out to me!\n\n"
            "I have received your message and will get back to you shortly.\n"
            "Meanwhile, feel free to check out my projects.\n\n"
            "Warm regards,\n"
            "Anitha N.T"
        )
        html_body = render_to_string("main/email/acknowledgement.html", {
            "name": name,
            "projects_url": f"{settings.SITE_URL}{reverse('projects')}",
        })
        ack = EmailMultiAlternatives(
            "Thank you for contacting Anitha 🌟", text_body, settings.EMAIL_HOST_USER, [email]
        )
        ack.attach_alternative(html_body, "text/html")
        ack.send()
        messages.success(
            request,
            "Your message has been sent successfully! A confirmation email has also been sent to you.",
        )
    except Exception:
        logger.exception("Contact form: could not send acknowledgement")
        messages.success(request, "Your message has been sent successfully!")

    return _section("contact")
