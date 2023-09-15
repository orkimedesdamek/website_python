# Website project
Simple website based on Python and Flask, uses MongoDB database, packed in Docker containers.
Uses Docker-Compose & Swarm to deploy services.
Git workflow is Gitflow.

## Version v1.01 20.07.2021
* Switched to gitflow workflow
* Minor changes

## Version v1.02 20.12.2021
* Deploy type switched to swarm stack deploy
* Docker images now stored in private registry
* Dockerfile security fixes
* Multiple other fixes and changes

## Version v1.03-v1.04 30.12.2021
* Separate Deploy stages for DEV and PROD now merged into single Deploy stage. DEV or PROD are defined by SERVICE_NAME and NODE_LABEL vars
* Variables are cleaned up from sh 
* DEV and PROD services now accesible only through node ip addresses it deployed on. (mode: host patameter in Compose yaml file)
* Defined services' deployment settings and resource management (restart policy, limits, mode etc. in Compose yaml file)
* Other minor fixes & cleanups 