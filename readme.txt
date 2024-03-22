#https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker

sudo docker build -t gcr.io/beaustory-417020/beaustory-image --no-cache .
sudo docker run -p 8501:8501 gcr.io/beaustory-417020/beaustory-image

gcloud auth configure-docker euurope-west3-docker.pkg.dev
docker push gcr.io/beaustory-417020/beaustory-image