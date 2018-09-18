<img src="img/playingDemo.gif?raw=true" width="300px" height="150px">

# Pygame + OpenCV Breakout-Game with Face Dectection
Pygame integrates with OpenCV to deploy pre-trained deep learning-based face detector.
The breakout game uses x-coordinate of a detected face to control the paddle.

## Prerequisites
The following software/packages are required to run this project.

* [Python3](https://www.python.org/)
* [OpenCV(3.3 or greater)](https://opencv.org/)
* [pygame(1.9.4 or greater)](https://www.pygame.org/docs/)
* [imutils (computer vision/image processing Python package created by the author of pyimagesearch.com)](https://github.com/jrosebr1/imutils)


## Running the game

```sh
$ python3 main.py -p deploy.prototxt.txt -m res10_300x300_ssd_iter_140000.caffemodel
```
OpenCV 3.3 ships with following ready-to-use deep learning-based face detector.

* ```deploy.prototxt.txt``` defines the architecture of pre-trained model
* ```res10_300x300_ssd_iter_140000.caffemodel``` is an actual pre-trained deep learning-based face detection model


more information about the face detector can be found [here](https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/)


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.) file for details

## Acknowledgments
The code on [post](https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/)([pyimagesearch](https://www.pyimagesearch.com/) by Adrian Rosebrock) is repurposed in ```face_detect.py```.

This project uses the following open-source art: 

* [The image used for the ball, bricks, paddle](https://opengameart.org/content/breakout-brick-breaker-tile-set-free)  
* [Background music](https://opengameart.org/content/wave-after-wave) by FoxSynergy
* Various sound effects are created on [Bfxr](https://www.bfxr.net/)
