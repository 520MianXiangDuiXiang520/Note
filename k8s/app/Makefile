
install:
	go build -o kube_app_demo .
	mv kube_app_demo $(GOBIN)

clean:
	rm $(GOBIN)/kube_app_demo

run:install
	$(GOBIN)/kube_app_demo

build_image:install
	bash deployment/docker/docker_build.sh

run_docker:
	 docker run -p 8080:8080 -d --name kube_demo kube_demo

stop_docker:
	docker stop kube_demo

.DEFAULT_GOAL := install