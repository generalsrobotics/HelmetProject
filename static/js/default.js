var display = document.getElementById('display');
var datetime = document.getElementById('datetime');
datetime.innerText = new Date().toLocaleString();
var distance = document.getElementById('distance');
var logo = document.getElementById('logo');
var feet = -1;
var demo = false;
var toggle_map = true;
var toggle_display = true;
var fullscreen = false;
var rgbLooper = null;
var viewLooper = null;
var toggle_rgb = true;

var params = new URLSearchParams(window.location.search);
if (params.has('demo')) {
  demo = true;
  rgbLooper = setInterval(function() {

    document.getElementById('light').onclick();
  }, 5000);
  viewLooper = setInterval(function() {

    window.location = (window.location.pathname === "/") ? "/point_cloud?demo=true" : "/?demo=true";
  }, 10000);
}

setInterval(function() {
      var update = new XMLHttpRequest();
      update.open("GET", '/info');
      update.send();

      update.onreadystatechange = (e) => {
        var msg = JSON.parse(update.responseText);
        distance.innerText = "Distance: " + msg.distance.toFixed(2) + " feet";
        document.body.style.background = col[msg.zone];
        window.navigator.vibrate([msg.zone * 300, msg.zone * 300]);
          if (demo) {
            logo.style.color = document.body.style.background;
            datetime.style.color = document.body.style.background;
            distance.style.color = document.body.style.background;

          }
        }
        datetime.innerText = new Date().toLocaleString();

      }, 300);

    var col = ['darkgreen', 'yellow', 'darkred'];

    var map = L.map("map").setView([40.838381, -73.938525], 20); L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
      maxZoom: 18,
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1
    }).addTo(map);

    function onLocationFound(e) {
      var radius = e.accuracy / 2;

      L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

      L.circle(e.latlng, radius).addTo(map);
    }

    function onLocationError(e) {

    }

    map.on('locationfound', onLocationFound); map.on('locationerror', onLocationError);

    map.locate({
      setView: true,
      maxZoom: 16
    });

    document.getElementById('map_icon').onclick = function() {
      toggle_map = !toggle_map;
      var m = document.getElementById('map');
      if (toggle_map) {
        m.style.display = 'block';
      } else {
        m.style.display = 'none';;
      }

    };

    var elem = document.documentElement;
    var fullscreen = false;
    /* View in fullscreen */
    function openFullscreen() {
      if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) {
        /* Firefox */
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) {
        /* IE/Edge */
        elem.msRequestFullscreen();
      }
    }

    /* Close fullscreen */
    function closeFullscreen() {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.mozCancelFullScreen) {
        /* Firefox */
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) {
        /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) {
        /* IE/Edge */
        document.msExitFullscreen();
      }
    }
    document.getElementById('misc').onclick = function() {
      fullscreen = !fullscreen;
      if (fullscreen) {
        openFullscreen();
      } else {
        closeFullscreen();
      }
    };

    document.getElementsByTagName('header')[0].onclick = function() {
      demo = !demo;

      if (demo) {
        rgbLooper = setInterval(function() {

          document.getElementById('light').onclick();
        }, 2000);
        viewLooper = setInterval(function() {

          window.location = (window.location.pathname === "/") ? "/point_cloud?demo=true" : "/?demo=true";
        }, 4000);
      } else {
        clearInterval(rgbLooper);
        clearInterval(viewLooper);
        logo.style.color = 'white';
        datetime.style.color = 'white';
        distance.style.color = 'white';
      }
    };
