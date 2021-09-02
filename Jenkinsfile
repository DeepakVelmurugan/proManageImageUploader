node{
    def ec2ip = "ssh -o  StrictHostKeyChecking=no ec2-user@65.2.148.5"
    stage('Git pull'){
       sshagent(['ec2-user']) {
           def clone = "${ec2ip} cd proManageImageUploader || ${ec2ip} git clone https://github.com/DeepakVelmurugan/proManageImageUploader.git;"
           sh "${ec2ip} sudo yum install git-all -y"
           sh "${clone}"
           sh "${ec2ip} git --git-dir=proManageImageUploader/.git pull"
           sh "${ec2ip}  mv * proManageImageUploader || echo Cannot copy directory"
       }
    }
    stage('Build docker image'){
        sshagent(['ec2-user']) {
            withCredentials([usernamePassword(credentialsId: 'accessID', passwordVariable: 'ACCESSKEY', usernameVariable: 'ACCESSID')]) {
                sh "${ec2ip} docker build --build-arg AWS_ACCESS_KEY_ID=$ACCESSID --build-arg AWS_SECRET_ACCESS_KEY=$ACCESSKEY -t deepakvelmurugan/promanageimageuploader:latest --file proManageImageUploader/Dockerfile ."    
            }
        }
    }
    stage('Push Docker Image'){
        sshagent(['ec2-user']) {
            withCredentials([usernamePassword(credentialsId: 'dockerCred', passwordVariable: 'dockerpwd', usernameVariable: 'deepakvelmurugan')]) {
                sh "${ec2ip} docker login -u ${deepakvelmurugan} -p ${dockerpwd}"
            }
            sh "${ec2ip} docker push deepakvelmurugan/promanageimageuploader"
        }
    }
    stage('Run Container on DEV server'){
        sshagent(['ec2-user']) {
            def dockerRemove = "docker rm -f imageuploader || echo Not found"
            def dockerRun = "docker run -p 8081:8001 -d --name imageuploader deepakvelmurugan/promanageimageuploader"
            sh "${ec2ip} ${dockerRemove}"
            sh "${ec2ip} ${dockerRun}"
        }
    }
}