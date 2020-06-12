document.addEventListener('DOMContentLoaded', () => {
  if ((sessionStorage.getItem("visited_login_page")!="true")) {
    document.getElementById("form_errors_displayed").style.display="none"
    sessionStorage.setItem("visited_login_page",true)
  }
});
