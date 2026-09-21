"""
Load (or refresh) the portfolio's project gallery:

    python manage.py seed_projects

Safe to run many times. Projects are matched by title; the title, image and live
link are set from the list below. Descriptions you write in /admin/ are never touched.
To add a project later, either add it here or use the admin.
"""

from django.core.management.base import BaseCommand

from main.models import Project

# (title, image file in media/projects/, live link)
PROJECTS = [
    ("Snapdeal Website", "snapdeal.jpg", "https://anitha250792.github.io/snapdealpage/snapdeal/signup.html"),
    ("Anitha Portfolio", "portfolio.jpg", "https://ani-portfolio-1.onrender.com/"),
    ("Fitnessfit Website", "fitnessfit.jpg", "https://anitha250792.github.io/fit/fitnessfit/index.html"),
    ("Ecommerce Website", "ecommerce.jpg", "https://anitha250792.github.io/ecommerce/"),
    ("Vetri Supermarket Billing Layout", "vetribilling.jpg", "https://anitha250792.github.io/vetribilling/"),
    ("Employee Payslip", "emppayslip.jpg", "https://anitha250792.github.io/Employeepay/Payslip/login.html"),
    ("Electrical Services Website", "electricservice.jpg", "https://anitha250792.github.io/services/Services/cctv.html"),
    ("Medical Billing Website", "medicalbilling.jpg", "https://anitha250792.github.io/medicalbilling/Medical%20billing/login.html"),
    ("Wedding Cards Website", "weddingcards.jpg", "https://anitha250792.github.io/weddingcards/Wedding%20Cards/login.html"),
    ("Online Cooking Website", "onlinecooking.jpg", "https://onlinecooking-1.onrender.com/"),
    ("Baby Products Website", "babyproducts.jpg", "https://baby-bliss-2.onrender.com/"),
    ("Bakery Website", "bakery.jpg", "https://bakery-i71a.onrender.com/"),
    ("Meditation Website", "meditation.jpg", "https://meditation-site-2.onrender.com/"),
    ("Stationery Website", "stationery.jpg", "https://stationary-website-4.onrender.com/"),
    ("Trading Website", "trading.jpg", "https://traco-website-4.onrender.com/partner/"),
    ("Bike Reselling Website", "bikeresell.jpg", "https://bike-resell.onrender.com/"),
    ("Shoe Ecommerce Website", "shoeecommerce.jpg", "https://footwear-frontend-two.vercel.app/"),
    ("AI/ML: Real-Time Weather Forecasting", "weatherforecast.jpg", "https://weather-frontend-two-plum.vercel.app/"),
    ("Cloud DevOps HRMS", "cloudhrms.jpg", "https://cloud-hrms-frontend-1.onrender.com"),
    ("Phishing URL Scan App", "phishingurl.jpg", "https://phishing-url-six.vercel.app/"),
    ("WhatsApp Integration", "whatsappintegration.jpg", "https://whatsapp-integration-frontend-green.vercel.app/"),
    ("Book Store", "bookstore.jpg", "https://book-store-rlmhx1yna-anitha250792s-projects.vercel.app/"),
    # NOTE: these two currently share the Book Store link. Replace with their own URLs.
    ("Car Wash", "carwash.jpg", "https://book-store-rlmhx1yna-anitha250792s-projects.vercel.app/"),
    ("Vegetable Shop", "vegshop.jpg", "https://book-store-rlmhx1yna-anitha250792s-projects.vercel.app/"),
]


class Command(BaseCommand):
    help = "Create or refresh the portfolio projects (title, image and live link)."

    def handle(self, *args, **options):
        created = updated = 0
        for title, image, link in PROJECTS:
            project = Project.objects.filter(title=title).first()
            if project is None:
                Project.objects.create(title=title, image=f"projects/{image}", link=link)
                created += 1
            else:
                project.image = f"projects/{image}"
                project.link = link
                project.save(update_fields=["image", "link"])
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Projects ready: {created} created, {updated} updated."))
