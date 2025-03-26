from django.db import models

class Event(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    no_of_members = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('closed', 'Closed')])
    no_of_members = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Member(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
