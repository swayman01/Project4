console.log("p4login.js")
document.addEventListener('DOMContentLoaded', () => {
  console.log("document loaded");
  console.log(sessionStorage.getItem("visited_login_page"));
  if ((sessionStorage.getItem("visited_login_page")!="true")) {
    document.getElementById("form-errors").style.display="none"
    sessionStorage.setItem("visited_login_page",true)
  }
});
