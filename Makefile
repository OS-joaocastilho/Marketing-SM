.PHONY: cluster cluster-down

cluster:
	ctlptl apply -f marketing_sm/infrastructure/manifests/cluster.yaml

cluster-down:
	ctlptl delete -f marketing_sm/infrastructure/manifests/cluster.yaml

docker-build:
	docker build . -f Dockerfile -t marketing-sm