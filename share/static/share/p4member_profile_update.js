document.addEventListener('DOMContentLoaded', () => {
  console.log("p4member_profile.js loaded");
  old_phone_number = document.getElementById("id_phone_number").value;
  //if ((old_phone_number[0]!=undefined)&&(old_phone_number[0]!=null)) {
  if (old_phone_number!="") {
  new_phone_number = phone_number_checkerJS(old_phone_number);
  if (!new_phone_number[0]) {
    document.getElementById("form_errors_displayed").innerText = new_phone_number[1];
  }
  if (new_phone_number[0]) {
      document.getElementById("form_errors_displayed").innerText = "";
      document.getElementById("id_phone_number").value = new_phone_number[1]
    }
  }
});

document.addEventListener('keyup', tel_check);
function tel_check(e) {
  old_phone_number = document.getElementById("id_phone_number").value;
  if ((old_phone_number[0]!=undefined)&&(old_phone_number[0]!=null)) {
     new_phone_number = phone_number_checkerJS(old_phone_number);
  if (!new_phone_number[0]) {
    document.getElementById("form_errors_displayed").innerText = new_phone_number[1];
  }
  if (new_phone_number[0]) {
      document.getElementById("form_errors_displayed").innerText = "";
      document.getElementById("id_phone_number").value = new_phone_number[1]
    }
  }
}

function phone_number_checkerJS(phone_number) {
  // Simple phone number checker and formatter. Checks for 10 digits and uses
  // dot format. Same function as Python version. JS version is because UpdateViews
  // are too difficult to modify
  var digits = /[0-9]/g;
  var phone_number_digits = phone_number.match(digits)
  if(phone_number_digits!=null) {
    if(phone_number_digits.length!=10) {
      fails_validation = [false,"Telephone number must contain 10 digits"];
      return fails_validation
    }
    else {
      var area_code = "";
      for (i=0;i<3;i++) {
        area_code = area_code + phone_number_digits[i];
      }
      var exchange = ".";
      for (i=3;i<6;i++) {
        exchange = exchange + phone_number_digits[i];
      }
      var subscriber = "."
      for (i=6;i<10;i++) {
        subscriber = subscriber + phone_number_digits[i]
      }
      tel_no = area_code + exchange + subscriber
      passes_validation = [true, tel_no]
      return passes_validation
    }
  }
}
