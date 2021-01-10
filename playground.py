import gtts
from gtts import gTTS

# myobj = gTTS(text="Witaj strudzony wędrowcze. Podaj swoje imię za 3 2 1 teraz", lang="pl", slow=False)
# myobj.save(f"audiofiles/unknownask.mp3")


myobj = gTTS(text="Istnieje już taki użytkownik. Podaj swoje imię za 3 2 1 teraz", lang="pl", slow=False)
myobj.save(f"audiofiles/notuniquename.mp3")