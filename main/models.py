from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200, default="Untitled Project")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects/")
    link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
