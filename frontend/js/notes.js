   document.addEventListener("DOMContentLoaded", function() {
        const title = document.getElementById("title");
        const newNoteBtn = document.getElementById("newNoteBtn");
        const notepad = document.getElementById("notepad");
  

        // LocalStorage'dan notları yükle
        const savedNotes = JSON.parse(localStorage.getItem("notes")) || [];
        savedNotes.forEach(note => {
            addNoteToList(note);
        });

        newNoteBtn.addEventListener("click", function() {
            const newNote = prompt("Enter new note title:");
            if (newNote) {
                addNoteToList(newNote);
                savedNotes.push(newNote);
                localStorage.setItem("notes", JSON.stringify(savedNotes)); // Notu kaydet
            }
        });
        // Notları listeye ekleyen fonksiyon
        function addNoteToList(note) {
            const li = document.createElement("li");
            li.textContent = note;

            // Silme butonunu oluştur
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Sil";
            deleteBtn.className = "deleteNoteBtn";
            deleteBtn.addEventListener("click", function(e) {
                e.stopPropagation(); // Silme butonuna tıklama olayının not tıklama olayını tetiklemesini engeller
                const noteIndex = savedNotes.indexOf(note);
                if (noteIndex > -1) {
                    savedNotes.splice(noteIndex, 1);
                    localStorage.setItem("notes", JSON.stringify(savedNotes)); // Notu LocalStorage'dan kaldır
                }
                li.remove(); // Notu sayfadan kaldır
            });

            li.appendChild(deleteBtn); // Silme butonunu liste elemanına ekle
            li.addEventListener("click", function() {
                notepad.value = note; // Notu textarea'ya yükle
            });

            title.appendChild(li);
        }
        document.getElementById("newNoteBtn").addEventListener("click", async function (event) {
            event.preventDefault();
            const title = document.getElementById("title").value;
            const description = document.getElementById("description").value;
        try{
            const response = await fetch("http://localhost:8000/notes_service/create_notes", {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                    body: JSON.stringify({
                        reciever_mail,
                        title,
                        description,
                    }),
                });

                const data = await response.json();
                console.log("API Yanıtı:", data);

                if(data.message=="Note created successfully"){
                    alert("başarıyla oluştu.");
                }
                else{
                    alert("Hata oluştu");
                }
            }catch (error){
                console.error("Hata:", error);
            }
        });
});
