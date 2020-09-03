# ServerlessFaceDetector
Using AWS serverless to build a web application for security measures. This project was focused to be implemented at daycare or preschools where secure measures are very much important such that the administration keeps monitoring always if it is the child`s parent who has come to drop off/pick up. Attached below are some of the screens that were developed as part of the project.

All the implementations were developed as microservices. The front end AJAX request called the API gateway which then triggers the respective lambda where the requirements are implemented and either saved to dynamoDB or S3 (based on different microservices).
