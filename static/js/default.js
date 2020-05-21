var display = document.getElementById('display');
var col = ["#00ff00", "#ffff00", "#ff0000"];
var ws = new WebSocket("ws://" + window.location.hostname + ":8000");
ws.onmessage = function(evt) {
  var range = evt.data;
  document.body.style.background = col[range];
};
var map = L.map("map").setView([40.838381, -73.938525], 20);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
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

map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);

map.locate({
  setView: true,
  maxZoom: 16
});

var toggle_map = true;
var toggle_display = true;
var fullscreen = false;


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
