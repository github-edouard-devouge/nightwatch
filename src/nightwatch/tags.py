import re
import os
import requests
import json
import dateparser
import datetime
import logging
from .models import TagFilter


TAG_FILTERS_JSON_CONF_FILE_PATH = os.getenv(
    "TAG_FILTERS_JSON_CONF_FILE_PATH", "/etc/nightwatch/tag-filters.json")


class NotSupportedRegistry(Exception):
    def __init__(self, message):
        super().__init__(message)


class CouldNotJoinRegitry(Exception):
    def __init__(self, message):
        super().__init__(message)


def getTagTS(tagName, tags):
    for tag in tags:
        if tag['name'] == tagName:
            return tag['start_ts']
    return


def getTags(registry, repository, credentials={}):
    tags = []

    def getHttp(uri, headers={}, params={}):
        r = requests.get(uri, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    try:

        # case Quay.io
        if "quay.io" in registry:
            uri = "https://quay.io/api/v1/repository/%s/tag/?onlyActiveTags=true" % (repository)
            registryInfos = getHttp(uri, headers={"X-Requested-With":""})
            for tag in registryInfos['tags']:
                tags.append(
                    {
                        "name": str(tag['name']),
                        "start_ts": datetime.datetime.fromtimestamp(tag['start_ts'])
                    }
                )
            return sorted(tags, key = lambda i: i['start_ts'], reverse=True)

        # case Dockerhub
        elif "docker.io" in registry:
            uri = "https://hub.docker.com/v2/repositories/%s/tags" % (repository)
            registryInfos = getHttp(uri)
            for tag in registryInfos['results']:
                tags.append(
                    {
                        "name": str(tag['name']),
                        "start_ts": dateparser.parse(tag['last_updated'])
                    }
                )
            return sorted(tags, key = lambda i: i['start_ts'], reverse=True)

        else:
            raise NotSupportedRegistry("Tags recuperation for %s is not implemented for this registry: %s" % (repository, registry))

    except (requests.RequestException, requests.HTTPError) as e:
        raise CouldNotJoinRegitry("Could not join this registry to retiewe tags: %s/%s" % (registry, repository))


def isValidTag(candidatTag, tagFilter):
    if tagFilter.operator == "include":
        return re.match(tagFilter.regex, candidatTag['name'])
    elif tagFilter.operator == "exclude":
        return not re.match(tagFilter.regex, candidatTag['name'])


def isEligibleFilter(registry, repository, tagFilter):
    if tagFilter:
        if tagFilter.scope == "global":
            return True
        elif tagFilter.scope == "repository":
            for item in tagFilter.scopedItems:
                if item == repository:
                    return True
        elif tagFilter.scope == "registry":
            for item in tagFilter.scopedItems:
                if item == registry:
                    return True
    return False


def getEligibleTags(registry, repository, tags):
    tagFilters = []
    try:
        with open(TAG_FILTERS_JSON_CONF_FILE_PATH) as json_file:
            data = json.load(json_file)
            for tagFilter in data['tag-filters']:
                tagFilters.append(TagFilter(**tagFilter))
    except IOError:
        logging.warning("Could not find tag-filters configuration file")

    if tags:
        candidatTags = []
        for candidatTag in tags:
            validTagFlag = True
            for filter in tagFilters:
                if filter and isEligibleFilter(registry, repository, filter):
                    if not isValidTag(candidatTag, filter):
                        validTagFlag = False
            if validTagFlag:
                candidatTags.append(candidatTag)
        if len(candidatTags) > 0:
            return sorted(
                candidatTags,
                key = lambda i: i['start_ts'],
                reverse=True
            )
    return []


def getYoungestTag(registry, repository, currentTagName, tags):
    currentTagTS = getTagTS(currentTagName, tags)
    for eligibleTag in getEligibleTags(registry, repository, tags):
        if eligibleTag['name'] != currentTagName:
            if currentTagTS and 'start_ts' in eligibleTag and eligibleTag['start_ts'] > currentTagTS:
                return eligibleTag
            elif not currentTagTS:
                return eligibleTag
            elif 'start_ts' not in eligibleTag:
                if eligibleTag['name'] > currentTagName:
                    return eligibleTag
    return
