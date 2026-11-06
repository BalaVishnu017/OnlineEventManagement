
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
                bat 'docker rm -f online-event-management-ci 2>NUL || ver >NUL'
                bat 'docker run -d --name online-event-management-ci -p 8082:80 online-event-management:1.0'
            }
        }

        stage('Install Selenium') {
    steps {
        bat '"C:/Program Files/Python314/python.exe" -m pip install -r requirements.txt'
    }
}

       
stage('Selenium Tests') {
    steps {
        bat 'powershell -NoProfile -Command "Start-Sleep -Seconds 5"'
        bat 'set BASE_URL=http://127.0.0.1:8082 && "C:/Program Files/Python314/python.exe" -m unittest discover -s tests -p "test_*.py" -v'
    }
}

    }

    post {
        always {
            bat 'docker rm -f online-event-management-ci 2>NUL || ver >NUL'
        }
    }
}
