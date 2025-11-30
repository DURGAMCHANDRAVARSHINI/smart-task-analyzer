from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    estimated_hours = models.FloatField(default=1.0)
    importance = models.IntegerField(default=5)
    dependencies = models.JSONField(default=list)

    def __str__(self):
        return f"{self.title} ({self.id})"


