pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "flask-app"  // Your image name
        CONTAINER_NAME = "flaskapp" // Your container name
        GIT_REPO = "https://github.com/Nandha172/My-docker-with-jenkinsproject.git"
    }

    stages {

        stage('Check Environment') {
            steps {
                script {
                    sh 'echo "Running on: $(hostname)"'
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    echo "Cloning repository..."
                    sh "rm -rf My-docker-with-jenkinsproject || true"
                    sh "git clone $GIT_REPO"
                    sh "cd My-docker-with-jenkinsproject"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image: $DOCKER_IMAGE"
                    sh "docker build -t $DOCKER_IMAGE My-docker-with-jenkinsproject/"
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    echo "Logging into Docker Hub using Jenkins Global Credentials..."
                    sh 'docker login'
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                script {
                    echo "Pushing image: $DOCKER_IMAGE"
                    sh "docker push $DOCKER_IMAGE"
                }
            }
        }

        stage('Cleanup Old Docker Images') {
            steps {
                script {
                    echo "Cleaning up unused Docker images..."
                    sh 'docker image prune -f || true'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    echo "Deploying container: $CONTAINER_NAME"
                    sh """
                    # Stop and remove existing container if running
                    if [ \$(docker ps -q -f name=$CONTAINER_NAME) ]; then
                        echo "Stopping existing container..."
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                    fi

                    # Remove existing image to ensure fresh pull
                    docker rmi -f $DOCKER_IMAGE || true

                    # Pull latest image and run
                    echo "Running new container..."
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $DOCKER_IMAGE
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully! 🎉'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}

