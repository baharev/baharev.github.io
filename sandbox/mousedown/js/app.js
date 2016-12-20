
function playAudio(event) {
  var img = document.getElementById(event.target.id);
  var audio_id = img.getAttribute('data-audio');
  var audio = document.getElementById(audio_id);
  audio.play();
}

document.addEventListener("touchstart", function() {}, false);

$(window).on('load', function() {
     var body = document.body;
     if (body.offsetHeight < body.scrollHeight ||
         body.offsetWidth  < body.scrollWidth) {
             var n = document.createTextNode(' ');
             var disp = body.style.display;
             body.appendChild(n);
             body.style.display = 'none';
             setTimeout(function(){
                 body.style.display = disp;
                 n.parentNode.removeChild(n);
             },20);
     }

     $('img').on('mousedown', playAudio);

     console.log('Callback added!')
});
