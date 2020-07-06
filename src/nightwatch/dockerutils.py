import re

GENERIC_REGISTRY_REGEX_PATTERN = "(.*[.][^/]*)/(.*)"
DEFAULT_DOCKER_REGISTRY = "docker.io"
DEFAULT_TAG = "latest"


def getRegistry(imageName):
    if re.match(GENERIC_REGISTRY_REGEX_PATTERN, imageName, re.IGNORECASE):
        return re.search(GENERIC_REGISTRY_REGEX_PATTERN, imageName, re.IGNORECASE).group(1)
    else:
        return DEFAULT_DOCKER_REGISTRY


def getTag(imageName):
    if ":" in imageName:
        return imageName.split(":")[1].split("@")[0]
    return DEFAULT_TAG


def getDigest(imageName):
    if "@" in imageName:
        return imageName.split("@")[1]
    return


def getRepository(imageName):
    if re.match(GENERIC_REGISTRY_REGEX_PATTERN, imageName, re.IGNORECASE):
        imageName = re.search(GENERIC_REGISTRY_REGEX_PATTERN, imageName, re.IGNORECASE).group(2)
    return imageName.split(":")[0]


def parseImage(imageName):
    return {
        "repository": getRepository(imageName),
        "registry": getRegistry(imageName),
        "tag": getTag(imageName),
        "digest": getDigest(imageName)
    }
