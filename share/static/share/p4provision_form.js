document.addEventListener('DOMContentLoaded', () => {
  console.log("p4provision_form.js loaded");
  remove_frequency_helptext()
});

function remove_frequency_helptext() {
  x=document.getElementById('id_frequency').parentNode
  if (x.childNodes[2].className=="helptext") {
    x.removeChild(x.childNodes[2]);
  }
}
