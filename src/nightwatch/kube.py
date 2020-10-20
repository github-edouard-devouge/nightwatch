from kubernetes import client, config


def appendImage(images, imageName, kubeResourceName, kubeResourceNamespace, kubeResourceKind):
    kubeResource = {
        'name': kubeResourceName,
        'namespace': kubeResourceNamespace,
        'kind': kubeResourceKind
    }
    kubeResources = [kubeResource]
    if imageName in images:
        images[imageName].extend(kubeResources)
    else:
        images[imageName] = kubeResources
    return images


def deduplicateImages(images):
    deduplicatedImages = {}
    for imageName in images:
        if imageName in deduplicatedImages:
            deduplicatedImages[imageName].extend(images[imageName])
        else:
            deduplicatedImages[imageName] = images[imageName]
    return deduplicatedImages


def appendPodImages(images):
    # list all pods image names
    coreV1 = client.CoreV1Api()
    ret = coreV1.list_pod_for_all_namespaces(watch=False)
    for pod in ret.items:
        for container in pod.spec.containers:
            images = appendImage(images, container.image, pod.metadata.name, pod.metadata.namespace, "pod")
    return images


def appendDeploymentsImages(images):
    appsV1 = client.AppsV1Api()
    # list all deployment image names
    ret = appsV1.list_deployment_for_all_namespaces(watch=False)
    for deployment in ret.items:
        for container in deployment.spec.template.spec.containers:
            images = appendImage(
                images,
                container.image,
                deployment.metadata.name,
                deployment.metadata.namespace,
                "deployment"
            )
    return images


def appendStatefulsetsImages(images):
    # list all sts image names
    appsV1 = client.AppsV1Api()
    ret = appsV1.list_stateful_set_for_all_namespaces(watch=False)
    for sts in ret.items:
        for container in sts.spec.template.spec.containers:
            images = appendImage(images, container.image, sts.metadata.name, sts.metadata.namespace, "statefulset")
    return images


def appendJobImages(images):
    batchV1 = client.BatchV1Api()
    # list all jobs image names
    ret = batchV1.list_job_for_all_namespaces(watch=False)
    for job in ret.items:
        for container in job.spec.template.spec.containers:
            images = appendImage(images, container.image, job.metadata.name, job.metadata.namespace, "job")
    return images


def appendCronjobImages(images):
    batchV1beta = client.BatchV1beta1Api()
    # list all cronjobs image names
    ret = batchV1beta.list_cron_job_for_all_namespaces(watch=False)
    for cron in ret.items:
        for container in cron.spec.job_template.spec.template.spec.containers:
            images = appendImage(images, container.image, cron.metadata.name, cron.metadata.namespace, "cronjob")
    return images


def appendDaemonsetImages(images):
    appsV1 = client.AppsV1Api()
    # list all cronjobs image names
    ret = appsV1.list_daemon_set_for_all_namespaces(watch=False)
    for ds in ret.items:
        for container in ds.spec.template.spec.containers:
            images = appendImage(images, container.image, ds.metadata.name, ds.metadata.namespace, "daemonset")
    return images


def getAllClusterImages():
    images = {}
    try:
        config.load_kube_config()
    except (IOError, config.config_exception.ConfigException) as e:
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException as e:
            raise Exception("Could not configure kubernetes python client: " + str(e))

    # get all container's image names for those kinds of k8s resources
    images = appendPodImages(images)
    images = appendDeploymentsImages(images)
    images = appendStatefulsetsImages(images)
    images = appendJobImages(images)
    images = appendCronjobImages(images)
    images = appendDaemonsetImages(images)

    # deduplicate imagesNames
    return deduplicateImages(images)
