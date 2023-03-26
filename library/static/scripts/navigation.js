var Open = true;
var fixed = true;

function openNav() {
    if (Open){
      document.getElementById("mySidebar").style.width = "250px";
      document.getElementById("main").style.marginLeft = "250px";
      Open = false;
      document.getElementById("openbtn").innerHTML = "&#9776; Close Sidebar";
      if (fixed){
        document.getElementById("main-footer-fixed").setAttribute("id","main-footer-sticky");
      }
      
    }
    else{
      closeNav();
    }
  }

function closeNav() {
    Open = true;
    document.getElementById("openbtn").innerHTML = "&#9776; Open Sidebar";
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    if (fixed){
      document.getElementById("main-footer-sticky").setAttribute("id","main-footer-fixed");
    }
  }
function adjustSidebar(){
    var flag = true;
    if (document.body.scrollHeight >= 900 && flag){
      document.getElementById("main-footer-fixed").setAttribute("id","main-footer-sticky");
      flag = false;
      fixed = false;
    }
  }
function adjustHeader(){
  var flag = true;
  if (document.scrollWidth > 900 && flag){
    var temp = document.body.scrollWidth.toString().concat("px")
    document.getElementById("header").style.width = temp;
  }
}