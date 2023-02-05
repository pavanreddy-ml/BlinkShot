# Blink Shot


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#code-explanation">Code Explanation</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a camera application that takes a picture of you when you blink your eyes

How to Use:
* Download the `shape_predictor_68_face_landmarks.dat` [here](https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat) and plate it in the same directory as BlinkShot.py.
* Change the 'save_photo' to `True` or `False` to save/not save the captures image.
* Run the BlinkShot.py file
* Close your eyes for two seconds. You should hear a beep.
* A countdown will appear on the screen and the image will be captured on 0. You have 3 seconds to smile or make a goofy face.
* The captured image will be displayed for 3 seconds

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

This project has been built with the following Frameworks/Libraries.

* [Python](https://www.python.org/)
* [OpenCV](https://opencv.org/releases/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Follow these steps to set up this project on your local machine.

### Prerequisites

Run the command to install openCV. New versions of OpenCV do not work with Intellisense

  ```sh
  pip install opencv-contrib-python==4.5.5.62
  ```

### Installation

Clone the repo
   ```sh
   git clone https://github.com/pavanreddy-ml/BlinkShot.git
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CODE EXPLANATION -->
## Code Explanation


<p align="right">(<a href="#code-explanation">back to top</a>)</p>
