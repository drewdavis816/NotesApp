from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
NOTE_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTE_FILE):
        with open(NOTE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as ex:
                print("Cannot retrieve file", ex)
                return []
    return []

def save_notes(notes):
    with open(NOTE_FILE, "w") as file:
        json.dump(notes, file, indent=4)


@app.route('/')
def index():
    notes = load_notes()
    return render_template("index.html", notes=notes)

@app.route('/create_note', methods=['POST'])
def create_note():
    note_title = request.form.get('note_title').strip()
    note_content = request.form.get('note_content').strip()

    if not note_title or not note_content:
        return redirect('/')

    notes = load_notes()

    # Check if note already exists
    for note in notes:
        if note["title"].lower() == note_title.lower():
            return redirect('/')

    notes.append({"title": note_title, "content": note_content})
    save_notes(notes)

    return redirect('/')

@app.route('/delete_note', methods=['POST'])
def delete_note():
    notes = load_notes()
    note_title = request.form.get('note_title').strip()

    if not note_title:
        return redirect('/')

    for i, note in enumerate(notes):
        if note["title"].lower() == note_title.lower():
            notes.pop(i)
            save_notes(notes)
            return redirect('/')

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)