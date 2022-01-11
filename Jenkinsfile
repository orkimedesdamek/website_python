pipeline {
    agent any

    environment {
        TAG = 'v1.04'
        COMPOSE_PROJECT_NAME = 'website_flask_mongo'
        DOCKER_CONTENT_TRUST = 1
        REGISTRY_NAME = '172.16.64.30:5000/'
    }

    stages {

        stage('Clone repository') {
            steps {
                checkout scm
            }
        }
        stage('Pylint test') {
            steps {
                sh "pylint  ./server/server.py | tee -a ./reports/pylint_report.txt" //Pylint test
            }
        }
        stage('Remove stack') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'master') {
                        SERVICE_NAME = 'service_PROD'
                        NODE_LABEL = "prod"
                    }
                    else {
                        SERVICE_NAME = 'service_DEV'
                        NODE_LABEL = "dev"
                    }
                }
                sh "docker stack rm ${SERVICE_NAME}"
                sh "sleep 10" //Need to replace this with waitUntil checking for stack containers delete
            }
        }
        stage('Remove old images') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') { 
                sh "docker image rm -f \$(docker image ls -f=reference=${REGISTRY_NAME}*:${TAG}-${BRANCH_NAME}* -q)"
                }
            }
        }
        stage('Compose image build') {
            steps {
                sh "docker-compose build"
            }
        }
        stage('Tests'){
            when { 
                anyOf { branch "release_*"; branch 'feature_*' }
                }
            steps {
                sh "/usr/local/bin/dockle ${REGISTRY_NAME}website_flask_server:${TAG}-${BRANCH_NAME}-${BUILD_NUMBER} | tee -a ./reports/dockle_report.txt" // Dockle test
                sh "/usr/local/bin/dockle ${REGISTRY_NAME}website_flask_mongo:${TAG}-${BRANCH_NAME}-${BUILD_NUMBER} | tee -a ./reports/dockle_report.txt"

                sh "/usr/local/bin/trivy ${REGISTRY_NAME}website_flask_server:${TAG}-${BRANCH_NAME}-${BUILD_NUMBER}| tee -a ./reports/trivy_report.txt" // Trivy test
                sh "/usr/local/bin/trivy ${REGISTRY_NAME}website_flask_mongo:${TAG}-${BRANCH_NAME}-${BUILD_NUMBER} | tee -a ./reports/trivy_report.txt"

//                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') { 
//                    sh '/usr/bin/hadolint ./server/Dockerfile | tee -a ./reports/hadolint_report.txt' // Hadolint test
//                    sh '/usr/bin/hadolint ./db/Dockerfile | tee -a ./reports/hadolint_report.txt'
//                }
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
        stage ('Deploy stack') {
            environment {
                NODE_LABEL = "${NODE_LABEL}"
            }
            steps {
//                ###This construction is better than passing USER PASSWORD to docker login, but did'nt work with insecure registries
//                script {    
//                  docker.withRegistry('192.168.100.12:5000', 'jenkins_registry_push') {
//                ###
//                withCredentials ([usernamePassword( credentialsId: 'jenkins_registry_push', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {    
//                    sh "docker login -u $USER -p $PASSWORD 192.168.100.12:5000"
//                    sh "docker-compose push" //Push images
//                    sh "docker stack deploy --compose-file docker-compose.yml --with-registry-auth ${SERVICE_NAME}"
//                }
            sh "docker-compose push" //Push images
            sh "docker stack deploy --compose-file docker-compose.yml"
            }
        }
    }
}   