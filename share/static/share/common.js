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
  if(document.getElementById(id_hidden).innerHTML!="") {
      form_errorsJSON = JSON.parse(document.getElementById(id_hidden).innerHTML);
    }
    errors = "";
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

  function format_dateJS(name) {
    //removes the hh-mm-ss from the first elementbyname. I would use getElementById
    //but it isn't easy in django
    let x = document.getElementsByName(name);
    x[0].value = x[0].value.slice(0,10);
  }
