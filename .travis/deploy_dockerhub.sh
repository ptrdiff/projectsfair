#!/bin/bash
if [[ "$TRAVIS_BRANCH" = "$RELEASE_BRANCH" && "$TRAVIS_PULL_REQUEST" = false ]] 
then
    TAG="latest"
    docker login -u $DOCKER_USER -p $DOCKER_PASS
    docker build -f Dockerfile -t $DOCKER_USER/$REPO_NAME:$TAG .
    docker push $DOCKER_USER/$REPO_NAME  
fi
