var map;

// This functions is used to plot the marker on google map. It returns the marker object
function plotMarker(Latitude, Longitude, map){

    var marker = new google.maps.Marker({
        position: {lat: Latitude, lng: Longitude},
    	map: map
    });

    return(marker);
    }

function myMap() {

    var mapCanvas = document.getElementById("map");
    var mapOptions = {
      center: new google.maps.LatLng(37.09024, -95.712891),
      zoom: 4,
    };

    map = new google.maps.Map(mapCanvas, mapOptions);

    if({{tweet_dict |safe}}){

        // Storing JSON data in the variable
        var tweetData = {{tweet_dict |safe}};
        var tweetsArray = tweetData.tweet;

        var data = [];
        if(tweetsArray.length > 0){

            var marker, i;
            var infowindow = new google.maps.InfoWindow();

            for(i = 0; i<tweetsArray.length; i++){

                var tweet = tweetsArray[i];
                // console.log("Lat: "+tweet.lat+"Log: "+tweet.long);
                marker = plotMarker(tweet.lat,tweet.long, map);

                google.maps.event.addListener(marker, 'click',

                    (function(marker, i){
                        return function() {

                            infowindow.setContent(tweetsArray[i].tweetData);
                            infowindow.open(map, marker);
                        }
                    }
                )(marker, i));
            }
            console.log(tweetsArray.length);
        }
        else {


            }
        }
        else{
            alert("the data is none");
        }
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
