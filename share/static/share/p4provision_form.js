document.addEventListener('DOMContentLoaded', () => {
  remove_frequency_helptext();
  format_dateJS("expiration_date");
});

function remove_frequency_helptext() {
  x=document.getElementById('id_frequency').parentNode
  if (x.childNodes[2].className=="helptext") {
    x.removeChild(x.childNodes[2]);
  }
}
