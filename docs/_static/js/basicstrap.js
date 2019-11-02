$(document).ready(function(){

  // Inline code styles to Bootstrap style.
  $('tt.docutils.literal').not(".xref").each(function (i, e) {
    // ignore references
    if (!$(e).parent().hasClass("reference")) {
      $(e).replaceWith(function () {
        return $("<code />").html($(this).html());
      });
  }});

  /*
   * Scroll the window to avoid the topnav bar
   * https://github.com/twitter/bootstrap/issues/1768
   */
  if ($(".navbar.navbar-fixed-top").length > 0) {
    // var navHeight = $(".navbar").height(),
    var navHeight = 40,
      shiftWindow = function() { scrollBy(0, -navHeight - 10); };
    if (location.hash) {
      setTimeout(shiftWindow, 1);
    }
    window.addEventListener("hashchange", shiftWindow);
  }

});