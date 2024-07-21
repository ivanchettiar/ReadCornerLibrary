from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
import uuid

# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    
    name =  models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre(e.g. Business, Personal Development, etc.)"
    )
 
    def get_absolute_url(self):
        """Return the url to access a particular genre instance."""
        return reverse("genre-detail", args=[str(self.id)])
    
    def __str__(self):
        """String output for representing the Model object."""
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint(
                    Lower("name"),
                    name="genre_name_case_insensitive_unique",
                    violation_error_message="Genre already exists (case insensitive match)"
            ),
        ]

class Language(models.Model):
    """Model representing a Language(e.g. English, Hindi, Spanish, etc.)"""

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the language of the book."
    )

    def get_absolute_url(self):
        """Return the url to access a particular language instance."""
        return reverse("language-detail", args=[str(self.id)])
    
    def __str__(self):
        """String output for representing the Model object."""
        return self.name
    
    

class Book(models.Model):
    """Model representing a book(unique entry in database)"""

    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books.
    author = models.ForeignKey('Author',on_delete=models.RESTRICT,null=True)
    # Author is mentioned as a string rather than object because it hasn't been declared yet in the file(Until this line).

    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief descripion of the book")
    isbn = models.CharField(
        'ISBN', 
        max_length=13,
        unique=True,
        help_text='Enter the 13 character ISBN number')
    #The first parameter in Charfield is called verbose_name. This will help set the name of the column as 'ISBN' instead of 'Isbn'

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book.")
    language = models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ", ".join(genre.name for genre in self.genre.all()[:3])
    
    #This below attricute assignment to the function helps set the column name in Admin Panel for this as Genre instead of 'Display Genre'.
    display_genre.short_description = "Genre"

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
    def __str__(self):
        """String output for representing the Model object."""
        return self.title
    

class BookInstance(models.Model):
    """Model Representing a specific copy of a book that can be borrowed from the library."""

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library")
    
    book = models.ForeignKey(Book,on_delete=models.RESTRICT,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    """
    M = Waiting to be stacked on the shelf.
    O = Book is already taken
    A = Can be taken
    R = Reserved to be borrowed but not yet taken
    """
    LOAN_STATUS = (
        ("M","Maintenance"),
        ("O","On Loan"),
        ("A","Available"),
        ("R","Reserved"),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="M",
        help_text="Book Availability"
    )
    #blank=True here means the Django will make this dropdown optional for user but it will explicitly add the default value "M"
    
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String output for representing the Model object."""
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    """Model representing an author"""

    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse("author-detail", args=[str(self.id)])
    
    def __str__(self):
        """String output for representing the Model object."""
        return f"{self.last_name}, {self.first_name}"