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
