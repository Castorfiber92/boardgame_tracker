class Player:
    def __init__(self, name: str, email: str = None):
        self.name = name
        self.email = email

    # Defines what is shown when the object is printed. 
    def __repr__(self):
        return f"Player(name={self.name!r})"