function deleteNote(noteId) {
<<<<<<< HEAD
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
=======
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4
}