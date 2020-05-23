document.addEventListener('DOMContentLoaded', () => {
  console.log("p4need.js loaded");
  remove_due_date_helptext()
  // id="id_type";  //Doesn't work 5/12/20
  // add_margin_top(id);
});

function remove_due_date_helptext() {
  x=document.getElementById("id_due_date").parentNode
  if (x.childNodes[2].className=="helptext") {
    x.removeChild(x.childNodes[2]);
  }
}
// function add_margin_top(id) { //Doesn't work 5/12/20
//    //TODO delete
//   document.getElementById(id).parentNode.parentNode.setAttribute("class", "add-margin-top");
// }
