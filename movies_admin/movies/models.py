import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class WorkType(models.TextChoices):
        MOVIE = _("movies")
        TV_SHOW = _("tv_show")

    title = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateTimeField(_("creation_date"))
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    type = models.CharField(_("type"), choices=WorkType.choices, max_length=10)

    file_path = models.CharField(_("file_path"), max_length=255)

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("film work")
        verbose_name_plural = _("film works")
        indexes = [
            models.Index(
                fields=["creation_date"],
                name="film_work_creation_date_idx",
            )
        ]

    def __str__(self):
        return self.title

    genres = models.ManyToManyField(Genre, through="GenreFilmWork")


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "genre_id"],
                name="film_work_genre",
            )
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self):
        return self.full_name

    film_works = models.ManyToManyField(FilmWork, through="PersonFilmWork")


class PersonFilmWork(UUIDMixin):
    class RoleType(models.TextChoices):
        ACTOR = _("actor")
        DIRECTOR = _("director")
        WRITER = _("writer")

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    role = models.CharField(_("role"), choices=RoleType.choices, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_idx",
            )
        ]
