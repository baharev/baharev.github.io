# Copyright (C) 2016 by Ali Baharev <ali.baharev@gmail.com>
# All rights reserved.
# BSD license.

from os import listdir

def main():
    images = sorted(f for f in listdir('images/') if f.endswith('.JPG'))
    print(', '.join(images))
    tiles = '\n'.join(to_tile(img) for img in images)
    with open('index.html', 'w') as f:
        f.write(PREAMBLE)
        f.write(tiles)
        f.write(POSTAMBLE)

def to_tile(img):
    return TILE.format(img)

TILE = \
'''
          <div class="tile">
              <span class="img_text">{0}</span>   
              <img src="images/{0}" alt="{0}"/>
          </div>
'''

PREAMBLE = \
'''<!doctype html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tiles</title>
    <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=PT+Serif">
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
          <p id="screen_size"> </p>
          <div id="filler"> </div>
        </div>
      </nav>

    <script type="text/javascript">
        /* Write screen size */
        window.onresize = displayWindowSize;
        window.onload = displayWindowSize;
        function displayWindowSize() {
            document.getElementById("screen_size").innerHTML = 
                "(" + window.innerWidth + "x" + window.innerHeight + ")";
        };
    </script>
      
      <div class="container">
'''

'''
          <div class="tile">
              <span class="img_text">alma</span>
              <img src="images/alma.jpg" alt=""/>
          </div>

          <div class="tile">
              <span class="img_text">bögre</span>
              <img src="images/bogre.jpg" alt=""/>
          </div>

          <div class="tile">
              <span class="img_text">borotva</span>
              <img src="images/borotva.jpg" alt=""/>
          </div>

          <div class="tile">
              <span class="img_text">cica</span>   
              <img src="images/cica.jpg" alt=""/>
          </div>
'''


POSTAMBLE = \
'''
      </div>
</body>
</html>
'''

if __name__ == '__main__':
    main()
