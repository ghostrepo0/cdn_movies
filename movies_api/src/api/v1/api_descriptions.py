page_info_string = """**page**: номер страницы \t
                       **size**: Сколько объектов вернуть \t"""

info = {
    "film_list": {
        "description": f"""На ней выводится список фильмов \t
                       {page_info_string}
                       **sort**: сортировка по полям, например, sort=-imdb_rating \t
                       **genre/actor**: это просто фильтрация, например, genre=<uuid:UUID>""",
        "summary": "Главная страница",
        "exception": "films not found",
    },
    "film_search": {
        "description": f"""На ней выводится список фильмов \t
                      {page_info_string}""",
        "summary": "Поиск по фильмам",
        "exception": "films not found"
    },

    "film_detail": {
        "description": "На ней выводится полная информация по фильму по id",
        "summary": "Полная информация по фильму",
        "exception": "film not found"
    },

    "genre_list": {
        "description": f"""На ней выводится список жанров \t
                        {page_info_string}
                       """,
        "summary": "Страница жанров",
        "exception": "genres not found"
    },
    "genre_search": {
        "description": f"""На ней выводится список жанров \t
                      {page_info_string}""",
        "summary": "Поиск по жанрам",
        "exception": "genres not found"
    },

    "genre_detail": {
        "description": "На ней выводится полная информация по жанру по id",
        "summary": "Полная информация по жанру",
        "exception": "genre not found"
    },

    "person_list": {
        "description": f"""На ней выводится список персон \t
                       {page_info_string}""",
        "summary": "Страница персон",
        "exception": "persons not found"
    },
    "person_search": {
        "description": f"""На ней выводится список персон \t
                      {page_info_string}""",
        "summary": "Поиск по персонам",
        "exception": "persons not found"
    },

    "person_detail": {
        "description": "На ней выводится полная информация по персоне по id",
        "summary": "Полная информация по персоне",
        "exception": "person not found"
    }
}
