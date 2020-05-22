var img = document.createElement('img');
img.id = "feed";
img.src = "/video_feed";
display.appendChild(img);
var width = 640;
var height = 480;
document.getElementById('video').onclick = function() {
  toggle_display = !toggle_display;

  if (toggle_display) {
    display.style.display = 'block';
  } else {
    display.style.display = 'none';
  }

};
document.getElementById('light').onclick = function() {
  toggle_rgb = !toggle_rgb;
  if (toggle_rgb) {
    img.src = '/video_feed';
  } else {
    img.src = '/depth_feed';
  }

};

document.getElementById('points').onclick = function() {
  window.location = "/point_cloud";

};

function onWindowResize() {
  img.width = window.innerWidth * 0.8;
  img.height = ((window.innerWidth * 0.8) / width) * height;


}
