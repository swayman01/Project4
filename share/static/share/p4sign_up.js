document.addEventListener('DOMContentLoaded', () => {
  clear_errorlist();
  form_errors("form_errors_hidden","form_errors_displayed","visited_sign_up_page")
  remove_confirm_password_helptext();
  email_phone_borders();
  password_help_text_format();
  move_bio_label();
});

function clear_errorlist() {
  document.querySelectorAll('.errorlist').forEach(function(a){
    a.remove();
  })}

 function remove_confirm_password_helptext() {
   x=document.getElementById('id_password2')
   if (x.parentNode.childNodes[4].className=="helptext") {
     x.parentNode.removeChild(x.parentNode.childNodes[4]);
   }
}

function email_phone_borders() {
  var plist = document.getElementsByTagName("P");
  var i_email = 0;
  for (i=0;i<plist.length;i++) {
    if (plist[i].innerText=="Email: ") {
      plist[i].setAttribute("class","borders-sides");
      i_email = i;
    }
    if (plist[i].innerText=="Phone or Text Number: ") {
      plist[i].setAttribute("class","borders-bottom-sides")
      i_phone = i;
    }
    x=document.getElementById("id_phone_number")
    x.setAttribute("type","tel")
  }
  let or_node = document.createElement("p");
  let or_node_text = document.createTextNode("Enter Email and Phone Number (optional):");
  or_node.setAttribute("class","borders-top-sides");
  or_node.setAttribute("class","borders-top-sides bold-centered")
  or_node.appendChild(or_node_text);
  plist[i_email].insertAdjacentElement('beforebegin', or_node);
}

function password_help_text_format() {
  ul_list = ullist = document.getElementById("info_a_form").querySelectorAll("ul");
  if (ul_list.length == 1) {
    index = 0;
  }
  else {
    index =2
  }
  ul_list[index].setAttribute("class","password_helptext_ul");
  li_list = ul_list[index].querySelectorAll("li");
  for (i=0;i<li_list.length;i++) {
    li_list[i].style.fontSize="smaller";
  }
}

function move_bio_label() {
  labellist = document.getElementsByTagName("LABEL")
  for (i=0;i<labellist.length;i++) {
    if (labellist[i].innerText=="Tell us about yourself:") {
      labellist[i].innerText="";
      i_label = i
    }
  }
  let bio_node = document.createElement("p");
  let bio_node_text = document.createTextNode("Tell us about yourself:");
  bio_node.setAttribute("class","bold-centered");
  bio_node.appendChild(bio_node_text);
  labellist[i_label].insertAdjacentElement('beforebegin', bio_node);
}
