load("ext://helm_remote", "helm_remote")

docker_build("marketing-sm", "", dockerfile="Dockerfile")

k8s_yaml("marketing_sm/infrastructure/manifests/app.yaml")

local_resource("gcp-credentials", "kubectl create secret generic gcp-credentials --save-config --dry-run=client --from-file=/Users/<USERNAME>/.config/gcloud/application_default_credentials.json -o yaml | kubectl apply -f -")

k8s_resource("marketing-sm", port_forwards=["8000:8000"])
