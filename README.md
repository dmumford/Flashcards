# Flashcard
#### Author: David Mumford
#### Version: 1.0.0

Flashcard is a simple program written in Python to review Chinese/English Flashcards.
Please note that this has been developed on Mac, so the TKinter label's may need 
re-positioning to run smoothly on Windows.

![GUI Screenshot](https://github.com/dmumford/Flashcards/blob/main/assets/img/Screenshot.png?raw=true)

## Flashcard Interface
* Chinese Character (Simplified)
* Romanised Pinyin
* Word Type (verb, noun, interjection, etc ..)
* English Translation(s)
* Flashcard ID number

### Buttons
* Press 1 to toggle between Chinese and English Audio
* Press 2 to toggle TTS Voices
* Press space to play audio
* Press r to go to random card in deck

### Navigation
There are two ways of Navigating through the Flashcards:

1. Clicking on 'arrow' buttons in the bottom-corners of the window.
2. Use the left and right arrows on your keyboard.

You can close the window using 'Esc' key on your keyboard.

### Searching for a Card
You can search for a Flashcard by typing the Flashcard ID number in the search box (top-right).

### Adding New Cards

This feature is a planned future development.
However, you can manually add custom decks by creating a new directory in 'assets/decks/'
with your desired deck name. You can then create a 'db.json' file within this new directory and
follow the file structure from another deck. To add audio to the deck, you can create two subdirectories in your
deck folder. One named 'zh' (for Chinese audio), and one named 'en' (for English audio). The naming convention
for the audio files are:

X.mp3 - audio voice 1
X_alt.mp3 - audio voice 2
X_alt2.mp3 - audio voice 3

...where 'X' is the card's ID number.

### Contributions
I welcome contributions to the Flashcards mini project!

Some ideas for development are:
* Toggle sliders to adjust audio playback speed
* Deck filtering
* Dynamic CRUD of Flashcards/Decks
* 1. Study mode - hide English meanings with reveal button to help user test knowledge
  2. Ability to add images to Flashcards to help user recall English meaning in Study mode
