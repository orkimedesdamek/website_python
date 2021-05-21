pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }
        stage('Remove old containers, networks, images etc.') {
            steps {
                sh 'docker-compose down --rmi all'
            }
        }
        stage('Compose image & container build') {
            steps {
                sh 'docker-compose up --no-start'
            }
        }
        stage('Tests'){
            steps {
        //    sh '/usr/local/bin/dockle website_flask_mongo:v1 | tee -a ./reports/dockle_report.txt' // Dockle test
            }
        }
        stage ('Container start') {
            steps {
                sh 'docker-compose start'
            }
        }
    }
}