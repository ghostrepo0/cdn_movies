from base_model import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: str
    full_name: str
