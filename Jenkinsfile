pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Docker Image') {
            steps { sh 'docker build -t online-event-management:latest .' }
        }
        stage('Run Application') {
            steps {
                sh 'docker rm -f online-event-management || true'
                sh 'docker run -d --name online-event-management -p 8081:80 online-event-management:latest'
            }
        }
        stage('Install Selenium') {
            steps { sh 'python3 -m pip install --user -r requirements.txt' }
        }
        stage('Selenium Tests') {
            steps { sh 'python3 -m unittest discover -s tests -p "test_*.py" -v' }
        }
    }
    post {
        always { sh 'docker rm -f online-event-management || true' }
    }
}
