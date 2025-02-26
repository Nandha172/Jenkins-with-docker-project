pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nandha172/flask-app"  // Docker Hub username added for push
        CONTAINER_NAME = "flaskapp"
        GIT_REPO = "https://github.com/Nandha172/Jenkins-with-docker-project.git"
    }

    stages {
        stage('Check Environment') {
            steps {
                script {
                    sh 'echo "Running on: $(hostname)"'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'Docker_hub_credentials',
                    usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PAT')]) {
                        sh "echo $DOCKER_PAT | docker login -u $DOCKER_USER --password-stdin"
                    }
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    echo "Cleaning old repo and cloning..."
                    sh "rm -rf Jenkins-with-docker-project || true"
                    sh "git clone $GIT_REPO"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image: $DOCKER_IMAGE"
                    sh "docker build -t $DOCKER_IMAGE Jenkins-with-docker-project/"
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

                    # Remove existing image
                    docker rmi -f $DOCKER_IMAGE || true

                    # Pull latest image from Docker Hub
                    docker pull $DOCKER_IMAGE

                    # Run the new container
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

