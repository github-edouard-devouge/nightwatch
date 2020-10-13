from kubernetes import client, config

images = {}


def appendImage(imageName, kubeResourceName, kubeResourceNamespace, kubeResourceKind):
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


def deduplicateImages():
    deduplicatedImages = {}
    for imageName in images:
        if imageName in deduplicatedImages:
            deduplicatedImages[imageName].extend(images[imageName])
        else:
            deduplicatedImages[imageName] = images[imageName]
    return deduplicatedImages


def getAllClusterImages():
    try:
        config.load_kube_config()
    except (IOError, config.config_exception.ConfigException) as e:
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException as e:
            raise Exception("Could not configure kubernetes python client: " + str(e))

    coreV1 = client.CoreV1Api()
    appsV1 = client.AppsV1Api()
    batchV1 = client.BatchV1Api()
    batchV1beta = client.BatchV1beta1Api()

    # list all pods image names
    ret = coreV1.list_pod_for_all_namespaces(watch=False)
    for pod in ret.items:
        for container in pod.spec.containers:
            appendImage(container.image, pod.metadata.name, pod.metadata.namespace, "pod")

    # list all deployment image names
    ret = appsV1.list_deployment_for_all_namespaces(watch=False)
    for deployment in ret.items:
        for container in deployment.spec.template.spec.containers:
            appendImage(
                container.image,
                deployment.metadata.name,
                deployment.metadata.namespace,
                "deployment"
            )

    # list all sts image names
    ret = appsV1.list_stateful_set_for_all_namespaces(watch=False)
    for sts in ret.items:
        for container in sts.spec.template.spec.containers:
            appendImage(container.image, sts.metadata.name, sts.metadata.namespace, "statefulset")

    # list all jobs image names
    ret = batchV1.list_job_for_all_namespaces(watch=False)
    for job in ret.items:
        for container in job.spec.template.spec.containers:
            appendImage(container.image, job.metadata.name, job.metadata.namespace, "job")

    # list all cronjobs image names
    ret = batchV1beta.list_cron_job_for_all_namespaces(watch=False)
    for cron in ret.items:
        for container in cron.spec.job_template.spec.template.spec.containers:
            appendImage(container.image, cron.metadata.name, cron.metadata.namespace, "cronjob")

    # deduplicate imagesNames
    return deduplicateImages()
