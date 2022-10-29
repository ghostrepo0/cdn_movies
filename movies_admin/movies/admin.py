from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_filter = ("name",)
    search_fields = ("name", "description", "id")


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline,)
    list_display = ("title", "type", "creation_date", "rating", "file_path")
    list_filter = (
        "type",
        "creation_date",
    )
    search_fields = ("title", "description", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmWorkInline,)
    list_display = ("full_name",)
    search_fields = ("full_name", "id")
