document.addEventListener('DOMContentLoaded', () => {
  remove_due_date_helptext()
    format_dateJS("due_date");
});

function remove_due_date_helptext() {
  x=document.getElementById("id_due_date").parentNode
  if (x.childNodes[2].className=="helptext") {
    x.removeChild(x.childNodes[2]);
  }
}
