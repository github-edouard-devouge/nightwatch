from prometheus_client import Gauge

IMAGES_INFOS = Gauge(
    'nightwatch_images',
    'Information about image tags',
    [
        'registry',
        'repository',
        'uuid',
        'current_tag',
        'current_tag_date',
        'target_tag',
        'target_tag_date'
    ]
)
IMAGES_CURRENT_TAG = Gauge(
    'nightwatch_images_current_tag_ts',
    'Timestamp of the current tag',
    (
        'registry',
        'repository',
        'uuid'
    )
)
IMAGES_TARGET_TAG = Gauge(
    'nightwatch_images_target_tag_ts',
    'Timestamp of the target tag',
    (
        'registry',
        'repository',
        'uuid'
    )
)

TOTAL_OUTDATED_IMAGES = Gauge(
    'nightwatch_outdated_images_total',
    'Total oudated images identified in kubernetes cluster',
)


def updateImageMetrics(images):
    TOTAL_OUTDATED_IMAGES.set(len(images))
    for image in images:
        currentTagDate = 0
        if hasattr(image.currentTag, 'start_ts') and image.currentTag.start_ts:
            currentTagDate = image.currentTag.start_ts.strftime('%s')
        targetTagDate = 0
        if hasattr(image.targetTag, 'start_ts') and image.targetTag.start_ts:
            targetTagDate = image.targetTag.start_ts.strftime('%s')
        targetTag = ""
        if hasattr(image.targetTag, 'name') and image.targetTag.name:
            targetTag = image.targetTag.name

        IMAGES_INFOS.labels(
            registry = image.registry.name,
            repository=image.repository,
            uuid=image.uuid,
            current_tag=image.currentTag.name,
            current_tag_date=currentTagDate,
            target_tag=targetTag,
            target_tag_date=targetTagDate
        ).set(1)
        IMAGES_CURRENT_TAG.labels(
            registry=image.registry.name,
            uuid=image.uuid,
            repository= image.repository
        ).set(currentTagDate)
        IMAGES_TARGET_TAG.labels(
            registry=image.registry.name,
            uuid=image.uuid,
            repository= image.repository
        ).set(targetTagDate)
