console.log("common.js");
function jsonSTR_to_array(jsonSTR){
  //This function takes a string that looks like an array of json objects and
  //converts it to a list
  //Strip leading and closing brackets ([])
  jsonSTR = jsonSTR.slice(1,-1);
  jsonLIST = jsonSTR.split("},");
  for (i=0;i<jsonLIST.length-1;i++){
    jsonLIST[i] = jsonLIST[i].concat("}");
  }
  for (i=0;i<jsonLIST.length;i++){
    jsonLIST[i] = JSON.parse(jsonLIST[i]);
  }
  return jsonLIST;
}

function form_errors(id_hidden,id_displayed,page){
  form_errorsJSON = "";
  console.log(id_hidden,id_displayed,page);
  console.log(document.getElementById(id_hidden).innerHTML);
  if(document.getElementById(id_hidden).innerHTML!="") {
      form_errorsJSON = JSON.parse(document.getElementById(id_hidden).innerHTML);
    }
    errors = "";
    console.log(page,sessionStorage.getItem(page));
    console.log(form_errorsJSON)
    if(((sessionStorage.getItem(page))=="true")&&(form_errorsJSON!="")) {
      for (const [key, value] of Object.entries(form_errorsJSON)) {
        for (i = 0; i < value.length; i++) {
          errors = errors.concat(value[i]);
          errors = errors.concat('<br>');
        }
      }

    }
  else {
      sessionStorage.setItem(page,true);
    }
    document.getElementById(id_displayed).innerHTML = errors;
  }
