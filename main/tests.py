from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Project


class LandingPageTests(TestCase):
    def setUp(self):
        Project.objects.create(title="Bakery Website", image="projects/bakery.png",
                               link="https://example.com/bakery")

    def test_home_renders_sections_and_narration(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        for section_id in ("about", "skills", "projects", "journey", "contact"):
            self.assertContains(response, f'id="{section_id}"')
        self.assertContains(response, "data-say=")
        self.assertContains(response, "Bakery Website")
        self.assertContains(response, 'id="console-data"')
        self.assertContains(response, "Languages: Python, JavaScript, HTML and CSS.")

    def test_old_urls_redirect_to_sections(self):
        self.assertRedirects(self.client.get(reverse("about")), "/#about", fetch_redirect_response=False)
        self.assertRedirects(self.client.get(reverse("projects")), "/#projects", fetch_redirect_response=False)
        self.assertRedirects(self.client.get(reverse("contact")), "/#contact", fetch_redirect_response=False)


class ContactFormTests(TestCase):
    payload = {"name": "Priya", "email": "priya@example.com", "message": "Hello!", "website": ""}

    def test_valid_post_sends_two_emails(self):
        response = self.client.post(reverse("contact"), self.payload)
        self.assertRedirects(response, "/#contact", fetch_redirect_response=False)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].reply_to, ["priya@example.com"])
        self.assertEqual(mail.outbox[1].to, ["priya@example.com"])

    def test_invalid_post_shows_errors(self):
        response = self.client.post(reverse("contact"), {"name": "", "email": "nope", "message": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-scroll="contact"')
        self.assertEqual(len(mail.outbox), 0)

    def test_honeypot_blocks_bots(self):
        self.client.post(reverse("contact"), {**self.payload, "website": "http://spam.example"})
        self.assertEqual(len(mail.outbox), 0)


class SeedProjectsTests(TestCase):
    def test_seed_creates_projects_and_is_idempotent(self):
        call_command("seed_projects", verbosity=0)
        self.assertEqual(Project.objects.count(), 24)
        call_command("seed_projects", verbosity=0)
        self.assertEqual(Project.objects.count(), 24)

    def test_seed_keeps_descriptions_written_in_admin(self):
        Project.objects.create(title="Bakery Website", description="My own text", image="old.png")
        call_command("seed_projects", verbosity=0)
        bakery = Project.objects.get(title="Bakery Website")
        self.assertEqual(bakery.description, "My own text")
        self.assertEqual(bakery.image.name, "projects/bakery.jpg")

    def test_journey_has_no_school_entries_or_scores(self):
        page = self.client.get(reverse("home")).content.decode()
        for word in ("SSLC", "Higher Secondary", "86.7", "Score:"):
            self.assertNotIn(word, page)
        self.assertIn("Bachelor of Technology", page)
