from django.db import models
from django.urls import reverse

# Choices
genre_choices = (
    ('classic', 'Classic'),
    ('romantic', 'Romantic'),
    ('comic', 'Comic'),
    ('fantasy', 'Fantasy'),
    ('horror', 'Horror'),
    ('educational', 'Educational'),
)

book_type_choices = (
    ('hardcover', 'Hard cover'),
    ('ebook', 'E-Book'),
    ('audiobook', 'Audiobook'),
)

class Book(models.Model):
    name = models.CharField(max_length=120)
    author_name = models.CharField(max_length=120, help_text="Author's name")
    price = models.FloatField(help_text='in US dollars $')
    genre = models.CharField(max_length=12, choices=genre_choices, default='classic')
    book_type = models.CharField(max_length=12, choices=book_type_choices, default='hardcover')
    notes = models.TextField(default="no notes...")
    pic = models.ImageField(upload_to='books/images', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        # This generates the URL for the detail view of this book
        return reverse('books:detail', kwargs={'pk': self.pk})
