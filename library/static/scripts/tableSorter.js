function removeText(){
  var text = document.getElementById("simple-book-header");
  if (text.innerText == "FLAG"){
    text.innerHTML = "Book Not Found<br>Click to go back";
    document.getElementById("temp").setAttribute("id","main-error");
    document.getElementById("simple-book-header").setAttribute("id","error-header");
    document.getElementById("error-header").setAttribute("onclick","goBack()");
  }
}

function navigate(){
  //Unimplemented 
}
function goBack(){
  window.history.back();
}
function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("bookTable");
    switching = true;
    dir = "asc"; 
    
    while (switching) {
      
      switching = false;
      rows = table.rows;
      
      for (i = 1; i < (rows.length - 1); i++) {
        
        shouldSwitch = false;
        
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        
        if (dir == "asc") {
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            
            shouldSwitch= true;
            break;

          }
        } else{
          if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {

            shouldSwitch = true;
            break;

          }
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        //Each time a switch is done, increase this count by 1:
        switchcount ++;      
      } else if (switchcount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  