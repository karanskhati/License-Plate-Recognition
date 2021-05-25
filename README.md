# Indian License Plate Detection || Mosaic'21 Round-2:
## Introduction:
This Project of automatic character recognition is used to detect Indian number plates from even the busiest streets and predict them to monitor unusual activities.<br/>
The project for the round 2 of Mosaic(IIT BHU ECE departmental fest) made us detect the plates first from any image then predict it. Methods of yolo is being implemented to achieve staggering result of license plate detection with an accuracy of 97.8%.<br/>
After which the project uses another yolo model to segment the given license plate into individual characters. Which is also supported by a sturdy 93%.<br/>
Internet has many state of the art ocr for predicting English characters and digits but we have developed a model by the process of transfer learning taking resnet layers to predict the segmented characters up to 96.7%.<br/>

## Yolo:
[This Repo was used to Train the Yolo models](https://github.com/TheKeH20/Training-Yolo-License-Plate-letter-Segmentation)

### The Dataset:
#### For Letter Segmentation:
[Original License Plate Dataset](https://www.kaggle.com/thamizhsterio/indian-license-plates "LP dataset")<br/>
333 Images from the above dataset were obtained and labelled in Yolo format using LabelImg Tool.
Check the link for labelled dataset 👇:<br/>
[Labelled Indian License Plate Dataset](https://www.kaggle.com/thekeh/indian-license-plate-letter-segmentation-dataset "Labelled Dataset")
#### For License Plate Detection:
[This Dataset was used for License Plate Detection](https://www.kaggle.com/andrewmvd/car-plate-detection)

## Key Features:
	1> Rotation Correction upto 45 Degrees
	2> Shadow Correction 
	3> Blurred Images are also read
These Features completes the given Problem Statement of Mosaic'21 Round-2.

## More Features:
	1> Multiple plates in a single frame.
	2> Video can also be processed to obtain results.
These Features completes the project and were used to score BONUS points.
	
## Running the Recognition Software:
All you need to do is Clone the Repo, Open the main(images).ipynb file-
Insert the image location in cv2.imread("<location>"),
Run the file :)
  
However this is only for images a seperate file named main(video).ipynb
  will also be provided for specific video file requirements.

HAPPY TESTING !!!!!!!!!!



## Team Blue-Cheese:

<table>
   <td align="center">
      <a href="https://github.com/TheKeH20">
         <img src="https://avatars.githubusercontent.com/u/60650819?v=4" width="100px;" alt=""/>
         <br />
         <sub>
            <b>Keshav Yadav</b>
         </sub>
      </a>
      <br />
   </td>
   <td align="center">
      <a href="https://github.com/aryanishan1001">
         <img src="https://avatars.githubusercontent.com/u/54237311?v=4" width="100px;" alt=""/>
         <br />
         <sub>
            <b>Aryan Ishan</b>
         </sub>
      </a>
      <br />
   </td>
   <td align="center">
      <a href="https://github.com/karanskhati">
         <img src="https://avatars.githubusercontent.com/u/77573210?v=4" width="100px;" alt=""/>
         <br />
         <sub>
            <b>Karan Singh Khati</b>
         </sub>
      </a>
      <br />
   </td>
</table>
