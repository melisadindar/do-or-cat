document.addEventListener("DOMContentLoaded", function() {
    const titleList = document.getElementById("title");
    const descriptionTextarea = document.getElementById("description");

    // LocalStorage'dan notları yükleme
    function loadNotesFromStorage() {
        const notesFromStorage = localStorage.getItem("notes");
        return notesFromStorage ? JSON.parse(notesFromStorage) : [];
    }

    // Notları LocalStorage'a kaydetme
    function saveNotesToStorage() {
        localStorage.setItem("notes", JSON.stringify(notes));
    }

    // Notları yükle
    let notes = loadNotesFromStorage();
    let activeNoteIndex = null;

    function loadNotes() {
        titleList.innerHTML = '';
        notes.forEach((note, index) => {
            const li = document.createElement("li");
            li.textContent = note.title;

            li.addEventListener("click", function() {
                descriptionTextarea.value = note.description;
                activeNoteIndex = index;
                setActiveTitle(index);
            });

            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.className = "deleteNoteBtn";
            deleteBtn.addEventListener("click", function(e) {
                e.stopPropagation();
                notes.splice(index, 1);
                saveNotesToStorage();
                loadNotes();
            });

            li.appendChild(deleteBtn);
            titleList.appendChild(li);
        });
    }

    function setActiveTitle(index) {
        const allTitles = titleList.querySelectorAll("li");
        allTitles.forEach((li, idx) => {
            if (idx === index) {
                li.classList.add("active");
            } else {
                li.classList.remove("active");
            }
        });
    }

    descriptionTextarea.addEventListener("input", function() {
        if (activeNoteIndex !== null) {
            notes[activeNoteIndex].description = descriptionTextarea.value;
            saveNotesToStorage();
        }
    });

    document.getElementById("newNoteBtn").addEventListener("click", function() {
        const newNoteTitle = prompt("Enter new note title:");
        if (newNoteTitle) {
            const newNote = { title: newNoteTitle, description: "" };
            notes.push(newNote);
            saveNotesToStorage();
            loadNotes();
            activeNoteIndex = notes.length - 1;
            descriptionTextarea.value = "";
        }
    });

    loadNotes();
});