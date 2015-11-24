$(document).ready(function() {
  var template = _.template(
    '<div><audio controls>\
      <source src="sounds/<%= filename %>" type="audio/wav">\
    </audio></div>');
  $.get('/sounds', function(d) {
    _.each(d.sounds, function(arg) {
      $('.container').append(template({filename: arg}));
    });
  });
});
