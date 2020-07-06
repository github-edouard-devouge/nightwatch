from kubernetes import client, config


def getAllClusterImages():
    imagesNames = []

    try:
        config.load_kube_config()
    except IOError:
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException as e:
            raise Exception("Could not configure kubernetes python client: " + e)

    coreV1 = client.CoreV1Api()
    batchV1 = client.BatchV1Api()
    batchV1beta = client.BatchV1beta1Api()

    # list all pods image names
    ret = coreV1.list_pod_for_all_namespaces(watch=False)
    for pod in ret.items:
        for container in pod.spec.containers:
            imagesNames.append(container.image)

    # list all jobs image names
    ret = batchV1.list_job_for_all_namespaces(watch=False)
    for job in ret.items:
        for container in job.spec.template.spec.containers:
            imagesNames.append(container.image)

    # list all cronjobs image names
    ret = batchV1beta.list_cron_job_for_all_namespaces(watch=False)
    for cron in ret.items:
        for container in cron.spec.job_template.spec.template.spec.containers:
            imagesNames.append(container.image)

    # deduplicate imagesNames
    return list(set(imagesNames))
