pipeline {
    agent any

    environment {
        TAG = 'v1.01'
        BUILD = '${BRANCH_NAME}_B${BUILD_NUMBER}'
        PREV_BUILD = '${BRANCH_NAME}_B$((BUILD_NUMBER-1))'
        COMPOSE_PROJECT_NAME = 'flask_website'

    }

    stages {
        stage ('Develop test') {
            when {
                branch 'develop'
            }
            steps {
                sh 'echo $BRANCH_NAME'
                sh 'echo $TAG'
                sh "echo ${BUILD}"
                sh "echo ${PREV_BUILD}"
                sh "echo ${COMPOSE_PROJECT_NAME}"
            }
        }
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }
        stage('Remove old containers, networks, images etc.') {
            steps {
                sh "TAG=${TAG} BUILD=${PREV_BUILD} docker-compose down --rmi all"
            }
        }
        stage('Compose image & container build') {
            steps {
                sh "TAG=${TAG} BUILD=${BUILD} docker-compose up  --no-start"
            }
        }
        stage('Tests'){
            when {
                anyOf { branch 'release'; branch 'master' }
            }
            steps {
                sh '/usr/local/bin/dockle website_flask_server:${TAG}-${BUILD} | tee -a ./reports/dockle_report.txt' // Dockle test
                sh '/usr/local/bin/dockle website_flask_mongo:${TAG}-${BUILD} | tee -a ./reports/dockle_report.txt'

                sh '/usr/local/bin/trivy website_flask_server:${TAG}-${BUILD} | tee -a ./reports/trivy_report.txt' // Trivy test
                sh '/usr/local/bin/trivy website_flask_mongo:${TAG}-${BUILD} | tee -a ./reports/trivy_report.txt'

                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') { 
                    sh '/usr/bin/hadolint ./server/Dockerfile | tee -a ./reports/hadolint_report.txt' // Hadolint test
                    sh '/usr/bin/hadolint ./db/Dockerfile | tee -a ./reports/hadolint_report.txt'
                }
                    
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