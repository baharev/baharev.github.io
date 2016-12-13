# Copyright (C) 2016 by Ali Baharev <ali.baharev@gmail.com>
# All rights reserved.
# BSD license.
from itertools import count
from os import listdir

def main():
    images = sorted(f for f in listdir('images/') if f.endswith('.JPG'))
    captions = image_captions()
    print(', '.join(images))
    tiles = '\n'.join(to_tile(*tup) for tup in zip(images, captions, count(1)))
    with open('index.html', 'w') as f:
        f.write(PREAMBLE)
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
          <audio id="audio{i}" src="audio/{i}.m4a" preload="auto" type="audio/mp4"></audio>

          <div class="tile">
              <span class="img_text">{caption}</span>
              <img src="images/{image}" alt="{image}" onclick="document.getElementById('audio{i}').play();"/>
          </div>
'''

PREAMBLE = \
'''<!doctype html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no, minimal-ui">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>Tiles</title>
    <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Roboto">
    <link rel="stylesheet" href="tiles.css">
    <script type='application/javascript'>
      document.addEventListener("touchstart", function() {}, false);
    </script>
</head>
<body>
      <nav>
        <div class="navlinks">
          <a href="">Home</a>
          <a href="">About</a>
          <a href="">Store</a>
          <a href="">Contact</a>
          <div id="filler"> </div>
        </div>
      </nav>
      
      <div class="container">
'''

POSTAMBLE = \
'''
      </div>
</body>
</html>
'''

if __name__ == '__main__':
    main()
