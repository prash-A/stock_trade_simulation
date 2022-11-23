pipeline {
    agent { docker { image 'python:3.10.1-alpine' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'perl --version'
                sh 'java --verion'
            }
        }
    }
}
