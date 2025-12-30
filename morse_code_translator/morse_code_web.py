from flask import Flask, request, render_template
import string

alphabet_to_morse = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-',
    'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
    'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
    'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': '/'
}

morse_to_alphabet = {v: k for k, v in alphabet_to_morse.items()}

app = Flask(__name__)

def is_morse(text):
    """Return True only if text looks like valid Morse"""
    return all(c in ".-/ \n" for c in text.strip())


def translate_to_morse(text):
    text = text.lower().replace("\n", " ")
    output = []

    for char in text:
        if char in alphabet_to_morse:
            output.append(alphabet_to_morse[char])
        elif char in string.punctuation:
            continue  
    return " ".join(output)


def translate_to_text(morse_code):
    morse_code = morse_code.replace("\n", " ").strip()
    words = morse_code.split(" / ")
    output_words = []

    for word in words:
        letters = word.split()
        decoded = ""
        for letter in letters:
            decoded += morse_to_alphabet.get(letter, "?")
        output_words.append(decoded)

    return " ".join(output_words)


@app.route("/", methods=["GET", "POST"])
def morse_translation():
    output = ""
    input_text = ""

    if request.method == "POST":
        input_text = request.form["input"]

        if is_morse(input_text):
            output = translate_to_text(input_text)
        else:
            output = translate_to_morse(input_text)

    return render_template(
        "index.html",
        input_text=input_text,
        output=output
    )


if __name__ == "__main__":
    app.run(debug=True)
