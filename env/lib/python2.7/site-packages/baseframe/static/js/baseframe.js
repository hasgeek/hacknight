// Activate chosen.js only if not on a mobile browser
// This is a global function. Isn't there a better way to do this?
function activate_chosen(selector) {
  if (!navigator.userAgent.match(/(iPod|iPad|iPhone|Android)/)) {
    $(selector).chosen({allow_single_deselect: true});
  }
}

$(function() {
  // Activate chosen on all 'select' tags.
  activate_chosen('select');

  var matchtab = function() {
    var url = document.location.toString();
    if (url.match('#/')) {
      $('.nav-tabs a[href=#'+url.split('#/')[1]+']').tab('show');
    } else if (url.match('#')) {
      $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show');
    }
  };

  // Load correct tab when fragment identifier changes
  $(window).bind('hashchange', matchtab);
  // Load correct tab when the page loads
  matchtab();
  // Change hash for tab click
  $('.nav-tabs a').on('shown', function (e) {
    window.location.hash = '#/' + e.target.hash.slice(1);
  });
  var url = document.location.toString();
  if (!url.match('#')) {
    // Activate the first tab if none are active
    $('.nav-tabs a').filter(':first').tab('show');
  }
});
