

// function for hiding and showing input fields. 1 out of 3 got disabled.
function yesnoCheck() {
    // if (document.getElementById('preselect').checked) {
    //     document.getElementById('ifpreselect').setAttribute("style", "visibility:visible;display:block;text-align:center;");
    //     document.getElementById('ifrss').setAttribute("style", "visibility:hidden;display:none;");
    //     document.getElementById('ifurl').setAttribute("style", "visibility:hidden;display:none;");
    // }
     if  (document.getElementById('rss').checked) {
        document.getElementById('ifpreselect').setAttribute("style", "visibility:hidden;display:none;");
        document.getElementById('ifrss').setAttribute("style", "visibility:visible;display:block;text-align:center;");
        document.getElementById('ifurl').setAttribute("style", "visibility:hidden;display:none;");
     }
    else if (document.getElementById('crawl').checked) {
        document.getElementById('ifpreselect').setAttribute("style", "visibility:hidden;display:none;");
        document.getElementById('ifrss').setAttribute("style", "visibility:hidden;display:none;");
        document.getElementById('ifurl').setAttribute("style", "visibility:visible;display:block;text-align:center;");

}
}