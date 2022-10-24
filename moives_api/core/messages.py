class FilmMessages:

    FILM_NOT_FOUND: str = "film not found".upper()
    FILMS_NOT_FOUND: str = "no films found".upper()

    FILMS_ALL_GET_SUMMARY: str = """
        GET all existing films
        """

    FILMS_ALL_GET_DESCRIPTION: str = """
        Запрос на получение всех фильмов:

        - **sort** : индекс для сортировки;
        """

    FILMS_ALL_GET_RESPONSE_DESCR: str = """
        Выдает все *доступные* в БД фильмы и краткую информацию по ним:

        - **id** : UUID фильма;
        - **title** : название фильма;
        - **imdb_rating** : рейтинг фильма;
        """

    FILMS_SEARCH_GET_SUMMARY: str = """
        SEARCH for film
        """

    FILMS_SEARCH_GET_DESCRIPTION: str = """
        Поиск фильма в Elasticsearch.
        """

    FILMS_SEARCH_GET_RESPONSE_DESCR: str = """
        Выдает все *подходящие* в БД фильмы и краткую информацию по ним:

        - **id** : UUID фильма;
        - **title** : название фильма;
        - **imdb_rating** : рейтинг фильма;
        """

    FILMS_ID_GET_SUMMARY: str = """
        GET film by ID
        """

    FILMS_ID_GET_DESCRIPTION: str = """
        Запрос полной информации о фильме по UUID:

        - **film_id** : UUID фильма;
        """

    FILMS_ID_GET_RESPONSE_DESCR: str = """
        Выдает полную информацию о фильме, если он существует в БД:

        - **id** : UUID фильма;
        - **tile** : название фильма;
        - **imdb_rating** : рейтинг фильма;
        - **type** : тип фильма (фильм/ТВ-шоу);
        - **description** : описание к фильму;
        - **genres** : жанр фильма;
        - **directors** : режиссер фильма;
        - **actors** : актеры;
        - **writers** : сценаристы.
        """


class GenreMessages:

    GENRE_NOT_FOUND: str = "genre not found".upper()
    GENRES_NOT_FOUND: str = "no genres found".upper()

    GENRES_ALL_GET_SUMMARY: str = """
        GET all existing genres
        """

    GENRES_ALL_GET_DESCRIPTION: str = """
        Запрос на получение всех жанров:

        - **sort** : индекс для сортировки;
        """

    GENRES_ALL_GET_RESPONSE_DESCR: str = """
        Выдает все *доступные* в БД жанры и краткую информацию по ним:

        - **id** : UUID жанра;
        - **name** : название жанра.
        """

    GENRES_SEARCH_GET_SUMMARY: str = """
        SEARCH for genre
        """

    GENRES_SEARCH_GET_DESCRIPTION: str = """
        Поиск жанра в Elasticsearch.
        """

    GENRES_SEARCH_GET_RESPONSE_DESCR: str = """
        Выдает все *подходящие* в БД жанры и краткую информацию по ним:

        - **id** : UUID жанра;
        - **name** : название жанра.
        """

    GENRES_ID_GET_SUMMARY: str = """
        GET genre by ID
        """

    GENRES_ID_GET_DESCRIPTION: str = """
        Запрос полной информации о жанре по UUID:

        - **genre_id** : UUID фильма;
        """

    GENRES_ID_GET_RESPONSE_DESCR: str = """
        Выдает полную информацию о жанре, если он существует в БД:

        - **id** : UUID жанра;
        - **name** : название жанра.
        """


class PersonMessages:

    PERSON_NOT_FOUND: str = "person not found".upper()
    PERSONS_NOT_FOUND: str = "no persons found".upper()

    PERSONS_ALL_GET_SUMMARY: str = """
        GET all existing persons
        """

    PERSONS_ALL_GET_DESCRIPTION: str = """
        Запрос на получение всех персоналий:

        - **sort** : индекс для сортировки;
        """

    PERSONS_ALL_GET_RESPONSE_DESCR: str = """
        Выдает все *доступные* в БД персоналии и краткую информацию по ним:

        - **id** : UUID персоны;
        - **name** : имя персоны.
        """

    PERSONS_SEARCH_GET_SUMMARY: str = """
        SEARCH for person
        """

    PERSONS_SEARCH_GET_DESCRIPTION: str = """
        Поиск персоналии в Elasticsearch.
        """

    PERSONS_SEARCH_GET_RESPONSE_DESCR: str = """
        Выдает все *подходящие* в БД персоналии и краткую информацию по ним:

        - **id** : UUID персоны;
        - **name** : имя персоны.
        """

    PERSONS_ID_GET_SUMMARY: str = """
        GET person by ID
        """

    PERSONS_ID_GET_DESCRIPTION: str = """
        Запрос полной информации о персоналии по UUID:

        - **person_id** : UUID фильма;
        """

    PERSONS_ID_GET_RESPONSE_DESCR: str = """
        Выдает полную информацию о персоне, если он существует в БД:

        - **id** : UUID персоны;
        - **name** : имя персоны.
        """
