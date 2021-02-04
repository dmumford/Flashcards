from cx_Freeze import setup, Executable

setup(name="Flashcards",
      version="1.0.1",
      description="",
      executables=[Executable("./flashcard.py")])
