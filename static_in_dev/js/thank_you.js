function myFunction() {
  var copyText = document.getElementById("copy_func");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  document.execCommand("copy");
}