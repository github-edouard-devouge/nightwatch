import logging
from uuid import uuid4

from .dockerutils import parseImage
from .models import Image, Registry, Tag, KubeResource
from .tags import NotSupportedRegistry, CouldNotJoinRegitry, getTags, getYoungestTag, getTagTS


def parse(imagesNames):
    images = []
    for imageName, kResources in imagesNames.items():
        kubeResources = []
        for resource in kResources:
            kubeResources.append(
                KubeResource(
                    name=resource['name'],
                    namespace=resource['namespace'],
                    kind=resource['kind']
                )
            )
        imageInfo = parseImage(imageName)
        images.append(
            Image(
                uuid=uuid4(),
                repository=imageInfo['repository'],
                registry=Registry(name=imageInfo['registry']),
                currentTag=Tag(name=imageInfo['tag']),
                kubeResources=sorted(kubeResources, key=lambda k: k.namespace)
            )
        )
    return images


def enrichTags(images):
    for image in images:
        try:
            availableTags = getTags(
                image.registry.name,
                image.repository,
                image.registry.credentials
            )
            if availableTags:
                image.availableTags = availableTags
                youngestTag = getYoungestTag(
                    image.registry.name,
                    image.repository,
                    image.currentTag.name,
                    availableTags
                )
                if youngestTag:
                    image.targetTag = Tag(**youngestTag)
                currentTagTs = getTagTS(
                    image.currentTag.name,
                    availableTags
                )
                if currentTagTs:
                    image.currentTag.start_ts = currentTagTs

        except (NotSupportedRegistry, CouldNotJoinRegitry) as e:
            logging.warning(e)
    return images
