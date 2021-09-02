# proManageImageUploader
<i>This repository is a part of proManage project.</i><br>
- It is maintained seperately since each one of them is treated as a micro-service.<br>
- This project follows <strong>Continuous integration and Continuous Deployment</strong> :recycle: and its isolated from other services by containerizing :lock: it.

## Micro-service details
#### Prerequistes 
- AWS account
- EC2 instance
- Jenkins in local machine

The image uploader uses REST APIs to upload, delete and get images from S3. S3 is the primary storage for storing image objects required/used in proManage project.

For API info refer this [Link](https://github.com/DeepakVelmurugan/proManageImageUploader/blob/master/API_Formats.txt)


