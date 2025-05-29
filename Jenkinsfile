pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:${env.PATH}"
        COMPOSER_HOME = "/tmp/composer"
        DOCKER_REGISTRY = "emmaekwere"
        INITIAL_VERSION = "1.0.0"
    }

    stages {
        stage('Check Build Trigger') {
            steps {
                script {
                    // CRITICAL: Stop infinite loop by checking if Jenkins triggered this build
                    def lastCommitAuthor = sh(
                        script: "git log -1 --pretty=format:'%an'",
                        returnStdout: true
                    ).trim()

                    def lastCommitMessage = sh(
                        script: "git log -1 --pretty=format:'%s'",
                        returnStdout: true
                    ).trim()

                    echo "🔍 Last commit author: ${lastCommitAuthor}"
                    echo "🔍 Last commit message: ${lastCommitMessage}"
                    echo "🔍 Build cause: ${currentBuild.getBuildCauses()}"

                    // Stop build if triggered by Jenkins CI commits
                    if (lastCommitAuthor == "Jenkins CI") {
                        echo "🛑 STOPPING BUILD - This was triggered by a Jenkins CI commit"
                        echo "🛑 This prevents infinite build loops"
                        currentBuild.result = 'ABORTED'
                        currentBuild.description = "Skipped - Jenkins CI automated commit"
                        error("Build skipped to prevent infinite loop.")
                    }

                    // Also check for [ci skip] or [skip ci] patterns
                    if (lastCommitMessage.toLowerCase().contains("[ci skip]") ||
                        lastCommitMessage.toLowerCase().contains("[skip ci]")) {
                        echo "🛑 STOPPING BUILD - Commit message contains skip instruction"
                        currentBuild.result = 'ABORTED'
                        currentBuild.description = "Skipped - [ci skip] in commit message"
                        error("Build skipped due to [ci skip] in commit message")
                    }

                    echo "✅ Build should proceed - triggered by legitimate code change"
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Detect Changed Services') {
            steps {
                script {
                    // Load service configurations from YAML file
                    def servicesConfig
                    if (fileExists('services-config.yaml')) {
                        servicesConfig = readYaml file: 'services-config.yaml'
                    } else {
                        // Fallback to hardcoded configuration
                        servicesConfig = [
                            services: [
                                'auth-service': [
                                    type: 'php',
                                    dockerfile: './auth-service/Dockerfile',
                                    deployment_file: './eks-deployment-setup/auth/deployment.yaml',
                                    container_name: 'auth-service'
                                ],
                                'job-apply-service': [
                                    type: 'python',
                                    dockerfile: './job-apply-service/Dockerfile',
                                    deployment_file: './eks-deployment-setup/jobs-applications/deployment.yaml',
                                    container_name: 'job-apply-service'
                                ],
                                'job-listing-service': [
                                    type: 'python',
                                    dockerfile: './job-listing-service/Dockerfile',
                                    deployment_file: './eks-deployment-setup/jobs-listing/deployment.yaml',
                                    container_name: 'job-listing-service'
                                ]
                            ]
                        ]
                    }

                    def services = servicesConfig.services

                    // Detect changed services
                    def changedServices = []

                    if (env.CHANGE_ID) {
                        // For Pull Requests - compare with target branch
                        def changedFiles = sh(
                            script: "git diff --name-only origin/${env.CHANGE_TARGET}...HEAD",
                            returnStdout: true
                        ).trim().split('\n')

                        services.each { serviceName, config ->
                            if (changedFiles.any { it.startsWith("${serviceName}/") }) {
                                changedServices.add(serviceName)
                            }
                        }
                    } else {
                        // For main branch builds - compare with previous commit
                        def changedFiles = sh(
                            script: "git diff --name-only HEAD~1 HEAD",
                            returnStdout: true
                        ).trim().split('\n')

                        services.each { serviceName, config ->
                            if (changedFiles.any { it.startsWith("${serviceName}/") }) {
                                changedServices.add(serviceName)
                            }
                        }
                    }

                    // If no changes detected or first build, build all services
                    if (changedServices.isEmpty()) {
                        echo "No service changes detected or first build - building all services"
                        changedServices = services.keySet().toList()
                    }

                    // Store results for later stages
                    env.CHANGED_SERVICES = changedServices.join(',')
                    env.SERVICES_CONFIG = writeJSON returnText: true, json: services

                    echo "Services to build: ${changedServices.join(', ')}"
                }
            }
        }

        stage('Build Services') {
            steps {
                script {
                    def changedServices = env.CHANGED_SERVICES.split(',')
                    def servicesConfig = readJSON text: env.SERVICES_CONFIG

                    // Build each changed service in parallel
                    def buildStages = [:]

                    changedServices.each { serviceName ->
                        buildStages[serviceName] = {
                            buildService(serviceName, servicesConfig[serviceName])
                        }
                    }

                    parallel buildStages
                }
            }
        }
    }

    post {
        success {
            echo 'Monorepo build pipeline succeeded!'
        }
        failure {
            echo 'Monorepo build pipeline failed!'
        }
        always {
            cleanWs()
        }
    }
}

def buildService(serviceName, serviceConfig) {
    stage("Build ${serviceName}") {
        echo "Building service: ${serviceName}"

        // Get next version for this service
        def version = getNextVersion(serviceName)
        def imageTag = "${env.DOCKER_REGISTRY}/${serviceName}:${version}"
        def latestTag = "${env.DOCKER_REGISTRY}/${serviceName}:latest"

        echo "Building ${serviceName} version ${version}"

        try {
            // Setup stage based on service type
            if (serviceConfig.type == 'php') {
                setupPhpService(serviceName)
                lintPhpService(serviceName)
                testPhpService(serviceName)
            } else if (serviceConfig.type == 'python') {
                setupPythonService(serviceName)
                lintPythonService(serviceName)
                testPythonService(serviceName)
            }

            // Build and push Docker image
            buildAndPushImage(serviceName, imageTag, latestTag)

            // Update deployment file
            updateDeploymentFile(serviceConfig.deployment_file, imageTag)

            // Tag the version in git
            tagVersion(serviceName, version)

            echo "Successfully built ${serviceName} version ${version}"

        } catch (Exception e) {
            error "Failed to build ${serviceName}: ${e.getMessage()}"
        }
    }
}

def getNextVersion(serviceName) {
    try {
        // Get the latest tag for this service
        def latestTag = sh(
            script: "git tag -l '${serviceName}-*' | sort -V | tail -n1",
            returnStdout: true
        ).trim()

        if (latestTag) {
            // Extract version number and increment patch version
            def version = latestTag.replace("${serviceName}-", "")
            def versionParts = version.split('\\.')
            def major = versionParts[0] as Integer
            def minor = versionParts[1] as Integer
            def patch = (versionParts[2] as Integer) + 1

            return "${major}.${minor}.${patch}"
        } else {
            // First build for this service
            return env.INITIAL_VERSION
        }
    } catch (Exception e) {
        echo "Error getting version for ${serviceName}, using initial version: ${e.getMessage()}"
        return env.INITIAL_VERSION
    }
}

def setupPhpService(serviceName) {
    dir(serviceName) {
        sh '''
            echo "Setting up PHP service..."
            echo "PHP Version:"
            /usr/local/bin/php --version
            echo "Composer Version:"
            /usr/local/bin/composer --version
            echo "Installing dependencies..."
            /usr/local/bin/composer install --no-interaction --prefer-dist --optimize-autoloader
        '''
    }
}

def lintPhpService(serviceName) {
    dir(serviceName) {
        sh '''
            if ! command -v phpcs >/dev/null 2>&1; then
                echo "Installing PHP CodeSniffer..."
                /usr/local/bin/composer global require 'squizlabs/php_codesniffer=*'
            fi
            export PATH=$PATH:/Users/spirit/.composer/vendor/bin
            LINT_DIRS=""
            [ -d "app" ] && LINT_DIRS="$LINT_DIRS app/"
            [ -d "routes" ] && LINT_DIRS="$LINT_DIRS routes/"
            [ -d "tests" ] && LINT_DIRS="$LINT_DIRS tests/"
            if [ -n "$LINT_DIRS" ]; then
                echo "Linting directories: $LINT_DIRS"
                /Users/spirit/.composer/vendor/bin/phpcs --standard=PSR12 $LINT_DIRS
            else
                echo "No directories to lint."
            fi
        '''
    }
}

def testPhpService(serviceName) {
    dir(serviceName) {
        sh '''
            if [ -f "./vendor/bin/pest" ]; then
                ./vendor/bin/pest
            elif [ -f "./vendor/bin/phpunit" ]; then
                echo "Pest not found, using PHPUnit instead"
                ./vendor/bin/phpunit
            else
                echo "No test runner found (pest or phpunit)"
                exit 1
            fi
        '''
    }
}

def setupPythonService(serviceName) {
    def pythonPath = sh(script: 'which python3', returnStdout: true).trim()
    def venv = "${env.WORKSPACE}/${serviceName}/venv"

    dir(serviceName) {
        sh """
            if [ ! -f requirements.txt ]; then
                echo "ERROR: requirements.txt not found in ${serviceName}"
                exit 1
            fi
            "${pythonPath}" -m venv "${venv}"
            . "${venv}/bin/activate"
            pip install --upgrade pip
            pip install -r requirements.txt
            pip freeze > requirements.lock
        """
    }
}

def lintPythonService(serviceName) {
    def venv = "${env.WORKSPACE}/${serviceName}/venv"

    dir(serviceName) {
        sh """
            . "${venv}/bin/activate"
            pip install flake8
            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv/,.*,__pycache__,docs/
        """
    }
}

def testPythonService(serviceName) {
    def venv = "${env.WORKSPACE}/${serviceName}/venv"

    dir(serviceName) {
        sh """
            . "${venv}/bin/activate"
            pip install pytest pytest-cov
            mkdir -p test-reports
            pytest --junitxml=test-reports/results.xml --cov=. --cov-report=xml:coverage.xml
        """

        // Publish test results
        junit allowEmptyResults: true, testResults: 'test-reports/results.xml'
        publishCoverage adapters: [coberturaAdapter(path: 'coverage.xml')]
    }
}

def buildAndPushImage(serviceName, imageTag, latestTag) {
    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DUMMY_USER', passwordVariable: 'DOCKER_TOKEN')]) {
        sh """
            echo \$DOCKER_TOKEN | docker login -u ${env.DOCKER_REGISTRY} --password-stdin

            # Build with version tag and latest tag
            docker build -t ${imageTag} -t ${latestTag} ./${serviceName}

            # Push both tags
            docker push ${imageTag}
            docker push ${latestTag}

            echo "Successfully pushed ${imageTag} and ${latestTag}"
        """
    }
}

def updateDeploymentFile(deploymentFile, imageTag) {
    def serviceName = imageTag.split('/')[1].split(':')[0]

    if (fileExists(deploymentFile)) {
        // Use the update script if available, otherwise fallback to sed
        if (fileExists('update-deployment.sh')) {
            sh """
                chmod +x update-deployment.sh
                ./update-deployment.sh "${deploymentFile}" "${imageTag}" "${serviceName}"
            """
        } else {
            sh """
                # Update the image tag in the deployment file
                sed -i.bak 's|image: ${env.DOCKER_REGISTRY}/${serviceName}:[^[:space:]]*|image: ${imageTag}|g' ${deploymentFile}

                # Show the changes
                echo "Updated ${deploymentFile} with new image: ${imageTag}"
                git diff ${deploymentFile} || true
            """
        }

        // FIXED: Commit and push the deployment file changes with correct email and detached HEAD handling
        // Add [ci skip] to prevent Jenkins from triggering itself
        sh """
            git config user.email "emaduilzjr1@gmail.com"
            git config user.name "Jenkins CI"
            git add ${deploymentFile}
            git commit -m "chore: update ${serviceName} deployment to ${imageTag} [ci skip]" || echo "No changes to commit"
            git push origin HEAD:main || echo "Failed to push deployment file changes"
        """
    } else {
        echo "Warning: Deployment file ${deploymentFile} not found."
    }
}

def tagVersion(serviceName, version) {
    sh """
        git config user.email "emaduilzjr1@gmail.com"
        git config user.name "Jenkins CI"
        git tag -a "${serviceName}-${version}" -m "Release ${serviceName} version ${version}"
        git push origin "${serviceName}-${version}" || echo "Failed to push tag"
    """
}