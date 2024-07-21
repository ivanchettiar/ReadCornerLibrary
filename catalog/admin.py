from django.contrib import admin
from .models import Genre, Language, Book, BookInstance, Author

# Register your models here.
"""Minimal registration of Models(Used when no customization is required in Admin panel for these models.)"""
admin.site.register(Genre)
admin.site.register(Language)

class BooksInstanceInline(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = BookInstance
    #If this extra was not adding, in the Books Detailed View you will get additional empty book instance rows. 
    #Adding extra=0 will show the records only if there are any book instances against this book/
    extra = 0

class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Administration object for Book models."""
    
    #We can't directly specify the genre field in list_display because it is a ManyToManyField (Django prevents this because there would be a large database access "cost" in doing so). 
    #Instead we'll define a display_genre function in Books class of models.py to get the information as a string.
    list_display = ['title','author','display_genre', 'language']

    inlines =[BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """Administration object for Book instance models."""
    list_display = ['book','status','due_back','id']
    list_filter = ['status','due_back']

    fieldsets = (
        (None, {
            'fields':('id','book','imprint')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Administration object for Author models."""

    list_display = ['last_name','first_name','date_of_birth','date_of_death']

    inlines = [BooksInline]