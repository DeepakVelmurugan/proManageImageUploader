FROM python:3.8-slim
WORKDIR /IMAGEUPLOAD
COPY . /IMAGEUPLOAD
# to install the requirements
RUN pip install --trusted-host pypi.python.org -r proManageImageUploader/requirements.txt
EXPOSE 8001
RUN cd /usr/local/bin
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_REGION="ap-south-1"
RUN aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
RUN aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
RUN aws configure set default.region $AWS_REGION
RUN mkdir -p images
CMD ["python3", "proManageImageUploader/app.py"]