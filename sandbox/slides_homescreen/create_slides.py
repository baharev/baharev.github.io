# Copyright (C) 2016 by Ali Baharev <ali.baharev@gmail.com>
# All rights reserved.
# BSD license.
from itertools import count
from os import listdir
from toolz import partition_all

def main():
    images = sorted(f for f in listdir('images/') if f.endswith('.JPG'))
    captions = image_captions()
    content = list(zip(images, captions, count(1)))
    step = 6
    size = len(content) // step
    for i, img_cap_idx_list in enumerate(partition_all(step, content)):
        create_slide(i, size, img_cap_idx_list)


def create_slide(i, size, img_cap_idx_list):
    tiles = '\n'.join(to_tile(*tup) for tup in img_cap_idx_list)
    fname = 'slide_{:02d}.html'
    prev, nxt = (i-1+size) % size, (i+1) % size
    prev, nxt = fname.format(prev+1), fname.format(nxt+1)
    with open(fname.format(i+1), 'w') as f:
        f.write(PREAMBLE.format(i=str(i+1), prev=prev, next=nxt))
        f.write(tiles)
        f.write(POSTAMBLE)


def image_captions():
    with open('text/captions.txt') as f:
        lines = [l.strip() for l in f]
    print(lines)
    return lines

def to_tile(image, caption, i):
    return TILE.format(image=image, caption=caption, i=str(i).zfill(2))

TILE = \
'''
          <audio id="audio{i}" src="audio/{i}.m4a"></audio>

          <div class="tile">
              <span class="img_text">{caption}</span>
              <img src="images/{image}" alt="{image}" onclick="document.getElementById('audio{i}').play();"/>
          </div>
'''

PREAMBLE = \
'''<!doctype html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimal-ui">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>Slide {i}</title>
    <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Roboto">
    <link rel="stylesheet" href="slides.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js">
    </script>
    <script type='application/javascript'>
      document.addEventListener("touchstart", function() {{}}, false);
      $(window).on('load', function() {{
           var n = document.createTextNode(' ');
           var body = document.body;
           var disp = body.style.display;
           body.appendChild(n);
           body.style.display = 'none';
           setTimeout(function(){{
               body.style.display = disp;
               n.parentNode.removeChild(n);
           }},100);
      }});
    </script>
</head>
<body>
    <div id="banner"></div>
    <nav>
      <div class="menubar">
          <div class="menuitem">
            <span onclick="$.get('{prev}',function(data){{var d=document.open('text/html','replace');d.write(data);d.close();}});">&#x21e6;&nbsp;Előző</span>
          </div>
          <div class="menuitem">
            <a href="index.html">&#x21bb;&nbsp;Kilépés</a>
          </div>
         <div class="menuitem">
            <span onclick="$.get('{next}',function(data){{var d=document.open('text/html','replace');d.write(data);d.close();}});">&#x21e8;&nbsp;Következő</span>
          </div>
      </div>
    </nav>
    <div class="centering">
      <div class="spring"> </div>
      <div class="container">
'''

POSTAMBLE = \
'''
      </div>
      <div class="spring"> </div>
   </div>
</body>
</html>
'''

if __name__ == '__main__':
    main()
