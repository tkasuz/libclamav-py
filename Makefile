DOCKER_IMAGE := clamav/clamav-debian
CONTAINER_NAME := clamav_container
LIB_PATH := /lib/libclamav.so.12.0.3
LOCAL_PATH := ./clamav/libclamav.so.12.0.3

.PHONY: copy-libclamav

copy-libclamav:
	rm -rf $(LOCAL_PATH)
	docker run --name $(CONTAINER_NAME) -d $(DOCKER_IMAGE) tail -f /dev/null
	docker cp $(CONTAINER_NAME):$(LIB_PATH) $(LOCAL_PATH)
	docker rm -f $(CONTAINER_NAME)
