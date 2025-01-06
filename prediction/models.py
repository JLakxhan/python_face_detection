from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)  # Title of the book
    description = models.TextField()  # Description of the book
    publication_date = models.DateField()  # Publication date of the book
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Foreign key to the Author model
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Book price, optional
    pages = models.IntegerField()  # Number of pages

    def __str__(self):
        return self.title