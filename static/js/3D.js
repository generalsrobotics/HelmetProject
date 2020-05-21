var scene, camera, renderer;
var geometry, mesh, material, texture, rgb;
var Wwidth = window.innerWidth * 0.8;
var Wheight = window.innerHeight * 0.8;

init();
animate();

function init() {

  camera = new THREE.PerspectiveCamera(50, Wwidth / Wheight, 1, 1000);
  camera.position.set(0, 0, 640);

  scene = new THREE.Scene();
  var width = 640,
    height = 480;


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








  renderer = new THREE.WebGLRenderer();
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(Wwidth, Wheight);
  display.appendChild(renderer.domElement);
  camera.position.set(0, 0, 1000);

  controls = new THREE.OrbitControls(camera, renderer.domElement);


  //
  window.addEventListener('resize', onWindowResize, false);

}

function onWindowResize() {

  camera.aspect = Wwidth / Wheight;
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
  if (material.uniforms.render_rgb.value) {
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
