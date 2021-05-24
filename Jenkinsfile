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
                sh 'BUILD=${BUILD_NUMBER} docker-compose up  --no-start'
            }
        }
        stage('Tests'){
            steps {
           // sh 'ls -l'
                sh '/usr/local/bin/dockle website_flask_server:v1 | tee -a ./reports/dockle_report.txt' // Dockle test
                archiveArtifacts artifacts: 'reports/*.txt' //Archiving build artifacts

                publishHTML (target: [ 
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'hadolint_report.txt,dockle_report.txt,trivy_report.txt',
                    reportName: 'Test reports',
                ]
                )
            }
        }
        stage ('Container start') {
            steps {
                sh 'docker-compose start'
            }
        }
    }
}