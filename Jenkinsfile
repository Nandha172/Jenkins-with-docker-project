pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nandha172/flask-app"
        CONTAINER_NAME = "flaskapp"
        GIT_REPO = "https://github.com/Nandha172/Jenkins-with-docker-project.git"
        GIT_BRANCH = "master" // Replace with your actual branch name
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
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-credential', 
                        usernameVariable: 'DOCKER_USER', 
                        passwordVariable: 'DOCKER_PAT'
                    )]) {
                        sh '''
                        echo "$DOCKER_PAT" | docker login -u "$DOCKER_USER" --password-stdin || exit 1
                        echo "Docker login successful!"
                        '''
                    }
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    echo "Cleaning old repo and cloning..."
                    sh '''
                    rm -rf Jenkins-with-docker-project || true
                    git clone -b $GIT_BRANCH $GIT_REPO || exit 1
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image: $DOCKER_IMAGE"
                    sh '''
                    docker build -t $DOCKER_IMAGE Jenkins-with-docker-project/ || exit 1
                    '''
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                script {
                    echo "Pushing image: $DOCKER_IMAGE"
                    sh '''
                    docker push $DOCKER_IMAGE || exit 1
                    '''
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
                    sh '''
                    if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                    fi

                    docker rmi -f $DOCKER_IMAGE || true

                    docker pull $DOCKER_IMAGE || exit 1

                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $DOCKER_IMAGE || exit 1
                    '''
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
