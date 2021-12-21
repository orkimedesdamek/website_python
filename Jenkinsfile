pipeline {
    agent any

    environment {
        TAG = 'v1.02'
//        BUILD = '${BRANCH_NAME}_B${BUILD_NUMBER}'
//        PREV_BUILD = '${BRANCH_NAME}_B$((BUILD_NUMBER-1))'
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
//                echo "Build is ${BUILD}"
                sh "docker-compose down --rmi all"
            }
        }
        stage('Compose image & container build') {
            steps {
                sh "docker-compose up  --no-start"
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
        stage ('DEV Push images to registry & Deploy stack') {
            when { 
                anyOf { branch "release_*"; branch 'feature_*'; branch 'develop' }
                }
            environment {
                NODE_LABEL = "dev"
            }
            steps {
//                ###This construction is better then passing USER PASSWORD to docker login, but didnt work with insecure registries
//                script {    
//                  docker.withRegistry('192.168.100.12:5000', 'jenkins_registry_push') {
//                ###
                withCredentials ([usernamePassword( credentialsId: 'jenkins_registry_push', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {    
                    sh "docker login -u $USER -p $PASSWORD 192.168.100.12:5000"
                    sh "docker-compose push" //Push images
                    sh "docker stack rm service_DEV"
                    sh "docker stack deploy --compose-file docker-compose.yml service_DEV"
                    sh "docker-compose down" //Delete compose containers, networks
                }
              } 
        }
        stage ('PROD Deploy stack') {
            when {
                anyOf { branch "master"; branch "hotfix_*" }
                }
            environment {
                NODE_LABEL = "prod"
            }
            steps {
//                ###This construction is better then passing USER PASSWORD to docker login, but didnt work with insecure registries
//                script {    
//                  docker.withRegistry('192.168.100.12:5000', 'jenkins_registry_push') {
//                ###
                withCredentials ([usernamePassword( credentialsId: 'jenkins_registry_push', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {    
                    sh "docker login -u $USER -p $PASSWORD 192.168.100.12:5000"
                    sh "docker-compose push" //Push images
                    sh "docker stack rm service_PROD"
                    sh "docker stack deploy --compose-file docker-compose.yml --with-registry-auth service_PROD"
                    sh "docker-compose down" //Delete compose containers, networks
                }
            }
        }
//        stage ('PROD Push images to local registry') {
//            when { 
//                anyOf { branch "master"; branch "prod_test" }
//                }
//            steps {
//                ###This construction is better then passing USER PASSWORD to docker login, but didnt work with insecure registries
//                script {    
//                  docker.withRegistry('192.168.100.12:5000', 'jenkins_registry_push') {
//                ###
//                withCredentials ([usernamePassword( credentialsId: 'jenkins_registry_push', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {    
//                    sh "docker login -u $USER -p $PASSWORD 192.168.100.12:5000"
//                    sh "REGISTRY_NAME=${REGISTRY_NAME} TAG=${TAG} BUILD=${BUILD} docker-compose push" //Push images
//                }
//              } 
//        }
    }
}   