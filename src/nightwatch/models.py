from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import List
from typing_extensions import Literal


class Tag(BaseModel):
    name: str
    start_ts: datetime = None

    class Config:
        schema_extra = {
             'example': [{
                'name': 'v1.0.3',
                'start_ts': datetime.now()
             }]
        }


class TagFilter(BaseModel):
    scope: Literal["global", "registry", "repository"] = "global"
    scopedItems: List[str] = None
    regex: str
    operator: Literal["include", "exclude"]

    class Config:
        schema_extra = {
             "example": [{
                "scope": "repository",
                "scopedItems": [
                    "grafana/grafana"
                ],
                "regex": ".*beta.*",
                "operator": "exclude"
             }]
        }


class Credentials(BaseModel):
    login: str = ""
    password: str = ""

    class Config:
        schema_extra = {
             'example': [{
                'login': 'admin',
                'password': '$ecret'
             }]
        }


class Registry(BaseModel):
    name: str
    credentials: Credentials = None

    class Config:
        schema_extra = {
             'example': [{
                'name': 'docker.io',
                'credentials': {
                    'login': 'admin',
                    'password': '$ecret'
                }
             }]
        }


class KubeResource(BaseModel):
    name: str
    namespace: str
    kind: str

    class Config:
        schema_extra = {
             'example': [{
                'name': 'prometheus-k8s',
                'namespace': 'kube-system',
                'kind': 'statefulset'
             }]
        }


class Image(BaseModel):
    uuid: UUID = uuid4()
    repository: str
    registry: Registry = None
    currentTag: Tag = None
    targetTag: Tag = None
    availableTags: List[Tag] = []
    kubeResources: List[KubeResource] = []

    class Config:
        schema_extra = {
             'example': [{
                'uuid': '16fd2706-8baf-433b-82eb-8c7faca847da',
                'repository': 'grafana/grafana',
                'registry': {
                    'name': 'docker.io',
                    'credentials': {
                        'login': 'admin',
                        'password': '$ecret'
                    },
                    'currentTag': {
                        'name': 'v1.0.3',
                        'start_ts': datetime.now()
                    },
                    'targetTag': {
                        'name': 'v1.0.4',
                        'start_ts': datetime.now()
                    },
                    'availableTags': [
                        {
                            'name': 'v1.0.3',
                            'start_ts': datetime.now()
                        },
                        {
                            'name': 'v1.0.4',
                            'start_ts': datetime.now()
                        }
                    ],
                    'kubeResources': [
                        {
                            'name': 'prometheus-k8s',
                            'namespace': 'kube-system',
                            'kind': 'statefulset.apps'
                        },
                        {
                            'name': 'pagerduty-exporter',
                            'namespace': 'monitoring',
                            'kind': 'deployment.apps'
                        }
                    ]
                }
             }]
        }
