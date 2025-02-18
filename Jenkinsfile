pipeline {
    agent any

    environment {
        REPO_URL = 'git@github.com:sofxcknboring/mu_bot.git'
        VDS_IP = '130.255.170.211'
        SSH_USER = 'ts3server'
        APP_NAME = ''
        BRANCH_NAME = ''
        DEPLOY_PROD = 'n'
    }

    stages {
        stage('Check Deploy Request') {
            steps {
                sshagent(['jenkins-ssh-key']) {
                    script {
                        def result = sh(script: "ssh -o StrictHostKeyChecking=no $SSH_USER@$VDS_IP 'cat /opt/deploy.flag || echo none'", returnStdout: true).trim()

                        if (result == "none") {
                            error("❌ Нет запроса на деплой, билд отменяется.")
                        }

                        def parts = result.split(" ")
                        BRANCH_NAME = parts[3].replace("BRANCH=", "")
                        DEPLOY_PROD = parts[4].replace("DEPLOY_PROD=", "")

                        APP_NAME = (BRANCH_NAME == 'dev') ? 'mu_bot_test' : 'mu_bot'

                        echo "🚀 Запрос на деплой: BRANCH=${BRANCH_NAME}, DEPLOY_PROD=${DEPLOY_PROD}, APP_NAME=${APP_NAME}"

                        // Удаляем флаг на VDS
                        sh "ssh $SSH_USER@$VDS_IP 'rm -f /opt/deploy.flag'"
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                script {
                    checkout([$class: 'GitSCM',
                        branches: [[name: "origin/${BRANCH_NAME}"]],
                        userRemoteConfigs: [[
                            url: REPO_URL,
                            credentialsId: 'github-ssh-key'
                        ]]
                    ])
                }
            }
        }

        stage('Deploy to VDS') {
            steps {
                sshagent(['jenkins-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $SSH_USER@$VDS_IP << EOF
                    set -e

                    echo "🔄 Pulling latest code from branch: ${BRANCH_NAME}..."
                    cd /opt/bots/$APP_NAME || { echo "❌ Error: Folder /opt/bots/$APP_NAME not found!"; exit 1; }
                    git reset --hard
                    git pull origin ${BRANCH_NAME}

                    echo "🐳 Building Docker image for ${APP_NAME}..."
                    docker build -t $APP_NAME .

                    echo "🛑 Stopping old container..."
                    docker stop $APP_NAME || true
                    docker rm $APP_NAME || true

                    echo "🚀 Starting new container..."
                    docker run -d --name $APP_NAME --restart=always $APP_NAME

                    echo "🧹 Cleaning up old Docker images..."
                    docker system prune -f

                    echo "✅ Deployment successful for ${APP_NAME}!"
                    EOF
                    """
                }
            }
        }
    }
}
