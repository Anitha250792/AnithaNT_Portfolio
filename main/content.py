"""
All portfolio text lives here.

Edit this file to change what the site shows *and* what the AI guide reads out:
every item that has a "say" value is rendered with a `data-say` attribute, and
the browser voice reads exactly that text (or, where there is no "say", the
text that is visible on the page).
"""


def join_words(items, conjunction="and"):
    """['a', 'b', 'c'] -> 'a, b and c' (reads naturally when spoken)."""
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + f" {conjunction} " + items[-1]


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------
PROFILE = {
    "name": "Anitha N.T.",
    "first_name": "Anitha",
    "location": "Chennai, India",
    "roles": [
        "Django Developer",
        "Python Developer",
        "Full Stack Developer",
        "Web Developer",
        "Frontend Developer",
        "Creative UI Developer",
        "Trainer & Technical Mentor",
    ],
    "tagline": "Full-stack Django developer building scalable, responsive and user-friendly web applications.",
}

INTRO_SAY = (
    "Welcome. I'm the AI guide for Anitha's portfolio. "
    "Anitha is a full-stack Django developer based in Chennai, India, "
    "who builds scalable, responsive and user-friendly web applications. "
    "Choose a topic to hear about her skills, projects and background, or play the full tour."
)

ABOUT = [
    # Paragraph 1: professional summary (from the CV).
    "Full-stack Django developer with hands-on experience building scalable web "
    "applications, including e-commerce platforms, booking systems and automation tools. "
    "Strong in backend development, REST APIs and database design, with the ability to "
    "deliver responsive, user-friendly interfaces.",
    # Paragraph 2: profile summary (refined from the original About text).
    "Detail-oriented Information Technology professional with a solid academic foundation "
    "and practical experience in programming, web development and modern frameworks. "
    "Adapts quickly to new tools and technologies, with proven problem-solving skills and "
    "a strong commitment to continuous learning. Seeking a challenging role in a progressive "
    "organization where technical expertise can add value and support professional growth.",
]

# ---------------------------------------------------------------------------
# Skills (original site + CV, merged)
# ---------------------------------------------------------------------------
_SKILLS = [
    ("Languages", "fa-code", "cyan", ["Python", "JavaScript", "HTML", "CSS"]),
    ("Web Development & Frameworks", "fa-globe", "violet",
     ["Django", "Flask", "React.js", "Bootstrap", "CSS", "HTML", "XHTML"]),
    ("Databases", "fa-database", "magenta", ["SQL", "MySQL", "SQLite"]),
    ("Tools & Libraries", "fa-screwdriver-wrench", "gold", ["Git", "VS Code", "xhtml2pdf"]),
    ("Core Concepts", "fa-diagram-project", "cyan",
     ["REST APIs", "Authentication", "Payment Integration (Razorpay)", "Responsive Design"]),
    ("Desktop Development", "fa-desktop", "violet", ["Tkinter"]),
    ("Operating Systems", "fa-computer", "magenta", ["Windows 10", "Linux"]),
    ("Professional Skills", "fa-people-group", "gold",
     ["Team collaboration", "Adaptability", "Quick learner"]),
]

SKILLS = [
    {
        "title": title,
        "icon": icon,
        "accent": accent,
        "items": items,
        "say": f"{title.replace('&', 'and')}: {join_words(items)}.",
    }
    for title, icon, accent, items in _SKILLS
]

# ---------------------------------------------------------------------------
# Project experience (from the CV)
# ---------------------------------------------------------------------------
# (title, alias, technologies, achievements)
# Technologies for PetPalooza, Employee Payslip Generator and Supermarket Billing come
# straight from the CV. The other three are based on the skills listed in the CV, so
# please confirm or edit them.
_EXPERIENCE = [
    ("Django E-commerce Platform", "PetPalooza",
     ["Python", "Django", "Razorpay", "Bootstrap"], [
        "Developed a full-featured e-commerce web application using Django",
        "Implemented user authentication, a shopping cart and Razorpay payment integration",
        "Built an order tracking system with shipment status updates and live location",
        "Designed a responsive user interface with Bootstrap",
    ]),
    ("Bike Reselling Marketplace", "",
     ["Python", "Django", "HTML", "CSS"], [
        "Built a platform for buying and selling used bikes",
        "Implemented product listings, filtering and user interaction features",
    ]),
    ("Employee Payslip Generator", "",
     ["Python", "Django", "xhtml2pdf"], [
        "Created a payroll system that generates automated PDF payslips",
        "Used a Django backend with xhtml2pdf for document generation",
    ]),
    ("Supermarket Billing System", "",
     ["Python", "Tkinter", "SQLite"], [
        "Developed a desktop billing application using Tkinter and SQLite",
        "Managed product inventory and billing calculations",
    ]),
    ("Electrical Service Booking Website", "",
     ["Python", "Django", "HTML", "CSS"], [
        "Built a service booking system with user registration and scheduling",
        "Implemented service request tracking and administrative management",
    ]),
    ("Recipe Sharing Website", "",
     ["Python", "Django", "HTML", "CSS"], [
        "Developed a recipe-sharing platform with search and filtering features",
    ]),
]

EXPERIENCE = []
for _i, (_title, _alias, _tech, _points) in enumerate(_EXPERIENCE):
    _lead = f"{_title}, known as {_alias}." if _alias else f"{_title}."
    EXPERIENCE.append({
        "title": _title,
        "alias": _alias,
        "tech": _tech,
        "points": _points,
        "accent": ["violet", "cyan", "magenta", "gold"][_i % 4],
        "featured": _i == 0,
        "say": _lead + " " + ". ".join(_points) + f". Technologies: {join_words(_tech)}.",
    })

# ---------------------------------------------------------------------------
# Journey: education, academic project, workshops, today
# ---------------------------------------------------------------------------
# NOTE: the old site says "Anna University, Virudhunagar" but the newest CV
# (Anitha_CCV.docx) says "Anna University, Tirunelveli". Change it here once.
BTECH_PLACE = "Anna University, Virudhunagar"

_ACADEMIC_POINTS = [
    "Implemented secure cloud storage with third-party auditing",
    "Applied homomorphic authenticators to ensure data integrity and privacy",
]
WORKSHOPS = ["Android Development", "MATLAB", "Network Technologies"]
GROWTH_AREAS = [
    "AI/ML weather forecasting",
    "a cloud DevOps HRMS",
    "phishing URL scanning",
    "WhatsApp integration",
]

JOURNEY = [
    {
        "year": "2014",
        "title": "Bachelor of Technology in Information Technology",
        "meta": BTECH_PLACE,
        "text": "Strong academic foundation in programming and web development.",
        "accent": "cyan",
        "say": "Anitha earned a Bachelor of Technology in Information Technology from "
               f"{BTECH_PLACE} in 2014, with a strong academic foundation in programming "
               "and web development.",
    },
    {
        "year": "Academic project",
        "title": "Secure Cloud Storage for Privacy-Preserving Public Auditing",
        "meta": "ASP.NET",
        "points": _ACADEMIC_POINTS,
        "accent": "violet",
        "say": "Academic project: Secure Cloud Storage for Privacy-Preserving Public Auditing, "
               "built with ASP.NET. " + ". ".join(_ACADEMIC_POINTS) + ".",
    },
    {
        "year": "Training",
        "title": "Workshops and Professional Development",
        "chips": WORKSHOPS,
        "accent": "magenta",
        "say": f"Professional development through workshops in {join_words(WORKSHOPS)}.",
    },
    {
        "year": "Focus",
        "title": "Full-Stack Django Development",
        "text": "Building scalable e-commerce platforms, booking systems and automation tools with Django.",
        "accent": "gold",
        "say": "Anitha's core focus is full-stack Django development, building scalable "
               "e-commerce platforms, booking systems and automation tools.",
    },
    {
        "year": "Now",
        "title": "Expanding into AI, Cloud and Integrations",
        "text": "Live projects now span AI/ML forecasting, a cloud DevOps HRMS, phishing URL "
                "detection and WhatsApp integration, deployed on Render, Vercel and GitHub Pages.",
        "accent": "cyan",
        "say": f"Recent projects extend into {join_words(GROWTH_AREAS)}, "
               "all deployed live on Render, Vercel and GitHub Pages.",
    },
]

# ---------------------------------------------------------------------------
# Resume band
# ---------------------------------------------------------------------------
LANGUAGES = ["Tamil", "English"]
STRENGTHS = ["Quick learner", "Adaptability", "Team collaboration"]
RESUME_SAY = (
    f"Languages: {join_words(LANGUAGES)}. "
    f"Core strengths: {join_words([s.lower() for s in STRENGTHS])}. "
    "The full CV is available to download."
)

# ---------------------------------------------------------------------------
# Contact channels
# ---------------------------------------------------------------------------
CONTACTS = [
    {"label": "Email", "value": "ntanithasaravanan@gmail.com",
     "url": "mailto:ntanithasaravanan@gmail.com", "icon": "fa-solid fa-envelope"},
    {"label": "Phone", "value": "+91 8939913838",
     "url": "tel:+918939913838", "icon": "fa-solid fa-phone"},
    {"label": "WhatsApp", "value": "Chat on WhatsApp",
     "url": "https://wa.me/918939913838", "icon": "fa-brands fa-whatsapp"},
    {"label": "LinkedIn", "value": "linkedin.com/in/anithant",
     "url": "https://www.linkedin.com/in/anithant", "icon": "fa-brands fa-linkedin-in"},
    {"label": "GitHub", "value": "github.com/Anitha250792",
     "url": "https://github.com/Anitha250792", "icon": "fa-brands fa-github"},
    {"label": "Location", "value": PROFILE["location"], "url": "", "icon": "fa-solid fa-location-dot"},
]
CONTACT_SAY = (
    "To get in touch, use the contact form, or reach Anitha by "
    + join_words(
        [c["label"] if c["label"] in ("LinkedIn", "GitHub", "WhatsApp") else c["label"].lower()
         for c in CONTACTS if c["label"] != "Location"],
        "or",
    )
    + ". All details are listed here."
)

# Social icons shown in the hero.
SOCIALS = [
    {"label": "LinkedIn", "url": "https://www.linkedin.com/in/anithant", "icon": "fa-brands fa-linkedin-in"},
    {"label": "GitHub", "url": "https://github.com/Anitha250792", "icon": "fa-brands fa-github"},
    {"label": "Instagram", "url": "https://instagram.com/aninta24", "icon": "fa-brands fa-instagram"},
    {"label": "Facebook", "url": "https://facebook.com/AnithaSaravanan", "icon": "fa-brands fa-facebook-f"},
]

# Resume file (in static/). Replace the PDF, keep the name – or change it here.
CV_STATIC_PATH = "main/files/Anitha_CV.pdf"


def landing_context():
    """Everything the landing page template needs besides DB projects and the form."""
    return {
        "profile": PROFILE,
        "intro_say": INTRO_SAY,
        "about": ABOUT,
        "skills": SKILLS,
        "experience": EXPERIENCE,
        "journey": JOURNEY,
        "languages": LANGUAGES,
        "strengths": STRENGTHS,
        "resume_say": RESUME_SAY,
        "contacts": CONTACTS,
        "contact_say": CONTACT_SAY,
        "socials": SOCIALS,
        "cv_path": CV_STATIC_PATH,
    }
