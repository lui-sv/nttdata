pipeline {
    agent any

    environment {
        // Ajusta si en tu agente se usa "py" en vez de "python"
        PYTHON = "C:/Users/Luis/AppData/Local/Programs/Python/Python310/python.exe"
        SONAR_HOST_URL = "http://localhost:9000"
        SONAR_PROJECT_KEY = "sqp_ec5e02d219969d0e5efd6efcd154a129531c0597"
    }

    stages {

        stage('Checkout') {
            steps {
                // Toma el código del repo configurado en el job
                checkout scm
            }
        }

        stage('Instalar dependencias') {
            steps {
                bat """
                %PYTHON% -m pip install --upgrade pip
                %PYTHON% -m pip install flask flask-cors
                """
            }
        }

        stage('Checks básicos') {
            steps {
                // Sólo verifica que el código Python compile
                bat """
                %PYTHON% -m compileall nttdata.py
                """
            }
        }

        stage('Análisis SonarQube') {
            steps {
                withCredentials([string(credentialsId: 'NTTDATA', variable: 'SONAR_TOKEN')]) {
                    bat """
                    pysonar ^
                      --sonar-host-url=%SONAR_HOST_URL% ^
                      --sonar-token=%SONAR_TOKEN% ^
                      --sonar-project-key=%SONAR_PROJECT_KEY%
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado (éxito o fallo)."
        }
        success {
            echo "✅ Build OK, análisis enviado a SonarQube."
        }
        failure {
            echo "❌ Build falló, revisar etapas en Jenkins."
        }
    }
}
