class BoardGame:
    def __init__(self, name: str):
        self.name = name

    # Defines what is shown when the object is printed. 
    def __repr__(self):
        return f"BoardGame(name={self.name})"
