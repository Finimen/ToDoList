from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=150, verbose_name="Title")
    content = models.CharField(max_length=255, verbose_name="Content")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    completed=  models.BooleanField(default=False, verbose_name="Completed")

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Priority")


    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="CreatedAt")

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['due_date'])
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def days_until_due(self):
        """How match days count still remain before a deadline"""
        if self.due_date:
            delta = self.due_date - timezone.now()
            return delta.days
        return None