document.addEventListener('DOMContentLoaded', () => {
  console.log("p4all_items.js loaded");
  //Test Code
  //var value = (document.getElementById('header').textContent);
  // var obj = JSON.parse('{ "name":"John", "age":30, "city":"New York"}');
  // console.log(obj)
  // var value = document.getElementById('header').textContent;
  // console.log("from <p> in html", value,value[2])
  // var value1 = document.getElementById('header1').textContent;
  // console.log("from <script text javascript", value1,value1[2])
  // var value2 = document.getElementById('header2').textContent;
  // console.log("from <script application/json", value2,value2[2])
  // var value3 = document.getElementById('header3').textContent;
  // console.log("from <script text javascript with safe filter", value3,value3[3])
  // valueJSON = JSON.parse(value3)
  // valueJSON1 = JSON.parse(value1) SyntaxError: Unexpected token v in JSON at position 0
  // valueJSON2 = JSON.parse(value2) SyntaxError: Unexpected token & in JSON at position 1
  // valueJSON3 = JSON.parse(value3)
  // End Test Code
  set_grid_columns()
  populate_grid()
});

function set_grid_columns() {
  var headerSTR = document.getElementById('header').textContent;
  var headerJSON = JSON.parse(headerSTR);
  var all_items_header_grid = document.getElementById("all_items_header_grid");
  var all_items_grid_class = "provisions-grid-"+headerJSON.length+"columns";
  all_items_header_grid.classList.add(all_items_grid_class);
  all_items_grid.classList.add(all_items_grid_class);
  for (i = 0; i < headerJSON.length; i++) {
    sp = document.createElement("span");
    let iplus1 = i+1;
    let class_name = "provision-column"+iplus1;
    sp.setAttribute("class",class_name);
    sp.setAttribute("class","bold-centered");
    sp.appendChild(document.createTextNode(headerJSON[i]))
    all_items_grid.appendChild(sp);
  }
}

function populate_grid() {
  var itemsSTR = document.getElementById('items').textContent;
  var itemsJSON = JSON.parse(itemsSTR);
  for (i = 0; i < itemsJSON.length; i++) {
    for (j = 0; j < itemsJSON[i].length; j++) {
      sp = document.createElement("span");
      let jplus1 = j+1;
      let class_name = "provision-column"+jplus1;
      sp.setAttribute("class",class_name);
      sp.appendChild(document.createTextNode(itemsJSON[i][j]))
      all_items_grid.appendChild(sp);
    }

  }

}
