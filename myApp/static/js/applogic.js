var map;

function myMap() {
  var mapCanvas = document.getElementById("map");
  var mapOptions = {
    center: new google.maps.LatLng(37.09024, -95.712891),
    zoom: 4,
  };

  map = new google.maps.Map(mapCanvas, mapOptions);
}

$(document).ready(function() {
  $('#dropdown-menu').on('change', function() {
     document.forms['myform'].submit();
  });
});




$('.dropdown-menu').on('click', 'a', function(e){

  // 'this' is the clicked anchor

  var text = this.text;
  var href = this.href;

  alert(text);

  // here add to local storage;

});
