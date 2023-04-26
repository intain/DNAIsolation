from django.db import models

# Create your models here.


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    pointOfContact = models.CharField(max_length=64)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Order(models.Model):
    number = models.IntegerField(primary_key=True)
    commissioner = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    contractor = models.CharField(
        max_length=16,
        choices=[
            ("Genomed", "Genomed"),
            ("A&A", "A&A")])
    finishDate = models.DateField()
    status = models.CharField(
        max_length=16,
        choices=[
            ("Oczekuje", "Oczekuje"),
            ("Otrzymano", "Otrzymano"),
            ("W realizacji", "W realizacji"),
            ("Wysłano", "Wysłano"),
            ("Zakończono", "Zakończono"),
            ("Anulowano","Anulowano")])
    notes = models.TextField()
    files = models.FileField(upload_to="uploads/%Y/%m/%d/", null=True)


class Material(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    unit = models.CharField(
       max_length=16, choices=[
            ("Liczba reakcji", "Liczba reakcji"),
            ("Zestaw", "Zestaw")])
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField()
    action = models.CharField(
        max_length=16, choices=[
            ("Dodanie", "Dodanie"),
            ("Usunięcie", "Usunięcie")])
    notes = models.TextField()


class LinkedFile(models.Model):
    file = models.FileField(upload_to="attachments/%Y/%m/%d/")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class SimpleFile(models.Model):
    name = models.CharField(max_length=64)
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")