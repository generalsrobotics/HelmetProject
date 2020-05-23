var scene, camera, renderer;
var geometry, mesh, material, texture, rgb;
var width = 640;
var height = 480;
var Wwidth = display.clientWidth;
var Wheight = display.clientHeight;

init();
animate();

function init() {

  camera = new THREE.PerspectiveCamera(50, Wwidth / Wheight, 1, 1000);


  scene = new THREE.Scene();



  geometry = new THREE.BufferGeometry();

  var vertices = new Float32Array(width * height * 3);

  for (var i = 0, j = 0, l = vertices.length; i < l; i += 3, j++) {

    vertices[i] = j % width;
    vertices[i + 1] = Math.floor(j / width);

  }

  geometry.addAttribute('position', new THREE.BufferAttribute(vertices, 3));





  rgb = new THREE.TextureLoader().load("/video_feed");

  texture = new THREE.TextureLoader().load("/depth_feed");
  texture.minFilter = THREE.NearestFilter;
  rgb.minFilter = THREE.NearestFilter;

  material = new THREE.ShaderMaterial({

    uniforms: {
      "rgb": {
        value: texture
      },
      "map": {
        value: texture
      },
      "width": {
        value: width
      },
      "height": {
        value: height
      },
      "pointSize": {
        value: 2
      },
      "zOffset": {
        value: 512
      },
      "render_rgb": {
        value: false
      }

    },
    vertexShader: document.getElementById('vs').textContent,
    fragmentShader: document.getElementById('fs').textContent,
    blending: THREE.AdditiveBlending,
    depthTest: false,
    depthWrite: false,
    transparent: true

  });
  mesh = new THREE.Points(geometry, material);
  scene.add(mesh);
  mesh.position.x -= 320;
  mesh.position.y -= 240;
  camera.position.set(0, 0, 960);







  renderer = new THREE.WebGLRenderer();
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(Wwidth, Wheight);
  display.appendChild(renderer.domElement);


  controls = new THREE.OrbitControls(camera, renderer.domElement);
renderer.domElement.id = "feed";


  //
  window.addEventListener('resize', onWindowResize, false);

}

function onWindowResize() {
  Wwidth = display.clientWidth;
  Wheight = display.clientHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(Wwidth, Wheight);

}



function animate() {

  requestAnimationFrame(animate);

  render();

}


function render() {
  if (material.uniforms.render_rgb.value) {
    rgb.needsUpdate = true;
  }

  texture.needsUpdate = true;
  controls.update();
  renderer.render(scene, camera);

}

document.getElementById('video').onclick = function() {
  window.location = "/";

};
document.getElementById('light').onclick = function() {
  toggle_rgb = !toggle_rgb;
  if (toggle_rgb) {
    material.uniforms.rgb.value = texture;
    material.uniforms.render_rgb.value = false;
  } else {
    material.uniforms.rgb.value = rgb;
    material.uniforms.render_rgb.value = true;
  }
};
document.getElementById('points').onclick = function() {
  toggle_display = !toggle_display;
  if (toggle_display) {
    display.style.display = "none";
  } else {
    display.style.display = "block";
  }

};
