pipeline {
  agent {
    label "docker-agent"
  }
  environment {
    HOST = "http://192.168.100.142"
    BRANCH= "v1"
    IMAGE_NAME= "simple-webserver"
  }
  stages {
    stage('Trufflehog') {
      steps {
        echo "Scanning..."
        // sh "docker run --rm -v $PWD:/pwd trufflesecurity/trufflehog:latest github --json --repo ${GIT_URL}"
      }
    }
    stage('Trivy Repo Scan'){
      steps{
        echo "Scanning..."
        // sh "trivy repository --branch ${BRANCH} ${GIT_URL}"
      }
    }
    stage('Stop and Remove Existing Containers') {
      steps {
        sh 'docker compose down'
      }
    }
    stage('Run Docker Compose') {
      steps {
        sh 'docker compose up -d --build'
      }
    }
    stage('Snyk Security') {
      steps {
        echo 'Testing...'
        // snykSecurity(snykInstallation: 'snyk@latest',snykTokenId: 'farukerdem34-snyk-api-token')
      }
    }
    stage('Trivy Docker Image Scan'){
      steps{
        echo "Trviy Docker Image Scan" 
        // sh "trivy image simple-webserver --severity HIGH,CRITICAL ${IMAGE_NAME}"
      }
    }
    stage('Zaproxy Baseline Scan') {
      steps {
        echo "Initializing baseling scan..."
        // sh "docker run -v ${PWD}:/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t ${HOST} -g gen.conf -r testreport.html"
        echo "Baseling scan completed succesfully"
      }
    }
  }
}
