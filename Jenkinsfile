pipeline {
    agent any

    environment {
        TAG = 'v1'

    }

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }
        stage('Remove old containers, networks, images etc.') {
            steps {
                sh 'BUILD=$((BUILD_NUMBER-1)) docker-compose down --rmi all'
            }
        }
        stage('Compose image & container build') {
            steps {
                sh 'BUILD=${BUILD_NUMBER} docker-compose up  --no-start'
            }
        }
 //       stage('Tests'){
 //           steps {
 //               sh '/usr/local/bin/dockle website_flask_server:${TAG}-B${BUILD_NUMBER} | tee -a ./reports/dockle_report.txt' // Dockle test
 //               sh '/usr/local/bin/dockle website_flask_mongo:${TAG}-B${BUILD_NUMBER} | tee -a ./reports/dockle_report.txt'
//
 //               sh '/usr/local/bin/trivy website_flask_server:${TAG}-B${BUILD_NUMBER} | tee -a ./reports/trivy_report.txt' // Trivy test
 //               sh '/usr/local/bin/trivy website_flask_mongo:${TAG}-B${BUILD_NUMBER} | tee -a ./reports/trivy_report.txt'
//
 //                   catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') { 
 //                   sh '/usr/bin/hadolint ./server/Dockerfile | tee -a ./reports/hadolint_report.txt' // Hadolint test
 //                   sh '/usr/bin/hadolint ./db/Dockerfile | tee -a ./reports/hadolint_report.txt'
 //               }
 //                   
 //               archiveArtifacts artifacts: 'reports/*.txt' //Archiving build artifacts
//
//                publishHTML (target: [ 
//                    allowMissing: false,
//                    alwaysLinkToLastBuild: false,
//                    keepAll: true,
//                    reportDir: 'reports',
//                    reportFiles: 'hadolint_report.txt,dockle_report.txt,trivy_report.txt',
//                    reportName: 'Test reports',
//                ]
//                )
//            }
//        }
        stage ('Container start') {
            steps {
                sh 'docker-compose start'
            }
        }
    }
}