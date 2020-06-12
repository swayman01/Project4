document.addEventListener('DOMContentLoaded', () => {

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
