-- создадим индекс по датам создания фильма
CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work(creation_date);

-- создадим композитный уникальный индекс по id_фильма и id_жанра
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre ON content.genre_film_work(film_work_id, genre_id);

-- создадим композитный уникальный индекс по id_фильма и id_актера и его роли
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work(film_work_id, person_id, role);
