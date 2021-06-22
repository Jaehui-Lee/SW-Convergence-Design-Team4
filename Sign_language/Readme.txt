Dockerfile_init으로 image 생성 후
Docker build -t sign_language_init:latest .

gcloud 설정한 후 commit
gcloud init -> login
Docker commit ps_name sign_language_gcloud

Dockerfile로 재실행
Docker build -t sign_language:latest .

Docker run -d -p 5000:5000 sign_language


Cloud upload
gcloud init
gcloud auth configure-docker
docker image tag sign_language:latest asia.gcr.io/automl-video-test-292702/sign_language
sudo docker push asia.gcr.io/automl-video-test-292702/sign_language:latest
