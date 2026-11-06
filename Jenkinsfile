
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t online-event-management:1.0 .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker rm -f online-event-management 2>NUL || ver >NUL'
                bat 'docker run -d --name online-event-management -p 8081:80 online-event-management:1.0'
            }
        }

        stage('Install Selenium') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Selenium Tests') {
            steps {
                bat 'python -m unittest discover -s tests -p "test_*.py" -v'
            }
        }
    }

    post {
        always {
            bat 'docker rm -f online-event-management 2>NUL || ver >NUL'
        }
    }
}
