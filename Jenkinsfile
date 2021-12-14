pipeline {
    agent any

    environment {
        TAG = 'v1.01'
        BUILD = '${BRANCH_NAME}_B${BUILD_NUMBER}'
        PREV_BUILD = '${BRANCH_NAME}_B$((BUILD_NUMBER-1))'
        COMPOSE_PROJECT_NAME = 'flask_website'
        DOCKER_CONTENT_TRUST = 1
        REGISTRY_NAME = '192.168.100.12:5000/'

    }

    stages {

        stage('Clone repository') {
            steps {
                checkout scm
            }
        }
        stage('Pylint test') {
            steps {
                //catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') { 
                sh "pylint  ./server/server.py | tee -a ./reports/pylint_report.txt" //Pylint test
                //}
            }
        }
        stage('Remove old containers, networks, images etc.') {
            steps {
                sh "COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} REGISTRY_NAME=${REGISTRY_NAME} TAG=${TAG} BUILD=${PREV_BUILD} docker-compose down --rmi all"
            }
        }
        stage('Compose image & container build') {
            steps {
                sh "COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} REGISTRY_NAME=${REGISTRY_NAME} TAG=${TAG} BUILD=${BUILD} docker-compose up  --no-start"
            }
        }
        stage('Tests'){
            when { 
                anyOf { branch "release_*"; branch 'feature_*' }
                }
            steps {
                sh "TAG=${TAG} BUILD=${BUILD} REGISTRY_NAME=${REGISTRY_NAME} /usr/local/bin/dockle ${REGISTRY_NAME}website_flask_server:${TAG}-${BUILD} | tee -a ./reports/dockle_report.txt" // Dockle test
                sh "TAG=${TAG} BUILD=${BUILD} REGISTRY_NAME=${REGISTRY_NAME} /usr/local/bin/dockle ${REGISTRY_NAME}website_flask_mongo:${TAG}-${BUILD} | tee -a ./reports/dockle_report.txt"

                sh "TAG=${TAG} BUILD=${BUILD} REGISTRY_NAME=${REGISTRY_NAME} /usr/local/bin/trivy ${REGISTRY_NAME}website_flask_server:${TAG}-${BUILD} | tee -a ./reports/trivy_report.txt" // Trivy test
                sh "TAG=${TAG} BUILD=${BUILD} REGISTRY_NAME=${REGISTRY_NAME} /usr/local/bin/trivy ${REGISTRY_NAME}website_flask_mongo:${TAG}-${BUILD} | tee -a ./reports/trivy_report.txt"

                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') { 
                    sh '/usr/bin/hadolint ./server/Dockerfile | tee -a ./reports/hadolint_report.txt' // Hadolint test
                    sh '/usr/bin/hadolint ./db/Dockerfile | tee -a ./reports/hadolint_report.txt'
                }
            }
        }
        stage ('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/*.txt' //Archiving build artifacts

                publishHTML (target: [ 
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'hadolint_report.txt,dockle_report.txt,trivy_report.txt,pylint_report.txt',
                    reportName: 'Test reports',
                ]
                )
            }
        }
        stage ('DEV Container start') {
            when { 
                anyOf { branch "release_*"; branch 'feature_*'; branch 'hotfix_*'; branch 'develop' }
                }
            steps {
                sh 'docker-compose start'
            }
        }
    
        stage ('PROD Push images to local registry') {
            when { 
                anyOf { branch "master"; branch "prod_test" }
                }
            steps {
//                ###This construction is better then passing USER PASSWORD to docker login, but didnt work with insecure registries
//                script {    
//                  docker.withRegistry('192.168.100.12:5000', 'jenkins_registry_push') {
//                ###
                withCredentials ([usernamePassword( credentialsId: 'jenkins_registry_push', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {    
                    sh "docker login -u $USER -p $PASSWORD 192.168.100.12:5000"
                    sh "REGISTRY_NAME=${REGISTRY_NAME} TAG=${TAG} BUILD=${BUILD} docker-compose push" //Push images
                }
              } 
        }
    }
//        stage ('PROD Pull from registry and container run') {
//            when {
//                anyOf { branch "master"; }
//                }
//            steps {
//
//            }
//        }
//    }
}   