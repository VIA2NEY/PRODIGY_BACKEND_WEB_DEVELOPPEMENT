from uuid import UUID

class User:
    def __init__(self, id: UUID, name: str, email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age