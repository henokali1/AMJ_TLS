from django.db import models
from datetime import date

class Client(models.Model):
    client_name = models.CharField(max_length=255)
    passport_no = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    age = models.IntegerField(editable=False)
    date = models.DateField(default=date.today)
    photo = models.ImageField(upload_to='client_photos/')

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client_name} ({self.passport_no})"

class ReportTemplate(models.Model):
    name = models.CharField(max_length=100)
    template_image = models.ImageField(upload_to='templates/')
    is_active = models.BooleanField(default=True)
    font_size = models.IntegerField(default=11, help_text="Font size for injected text (e.g. 11 for standard Calibri)")
    
    # Coordinates
    name_x = models.IntegerField(default=0)
    name_y = models.IntegerField(default=0)
    passport_x = models.IntegerField(default=0)
    passport_y = models.IntegerField(default=0)
    age_x = models.IntegerField(default=0)
    age_y = models.IntegerField(default=0)
    date_x = models.IntegerField(default=0)
    date_y = models.IntegerField(default=0)
    
    # Photo corners (2 Points: Top-Left and Bottom-Right)
    photo_x1 = models.IntegerField(default=0)
    photo_y1 = models.IntegerField(default=0)
    photo_x2 = models.IntegerField(default=0)
    photo_y2 = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.is_active:
            ReportTemplate.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
