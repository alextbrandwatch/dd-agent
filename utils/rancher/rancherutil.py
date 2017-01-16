import logging
import requests

from utils.singleton import Singleton

log = logging.getLogger('collector')


class RancherUtil:
    __metaclass__ = Singleton

    RANCHER_METADATA_URL = 'http://rancher-metadata/'
    METADATA_VERSION = '2016-07-29'
    CONTAINERS_PATH = 'containers'

    def get_ports_for_container(self, container_name):
        rancher_metadata_url = ('%s/%s/%s/%s/%s' % (self.RANCHER_METADATA_URL,
                                                    self.METADATA_VERSION,
                                                    self.CONTAINERS_PATH,
                                                    container_name,
                                                    'ports'))

        headers = {'Accept': 'application/json'}

        response = requests.get(url=rancher_metadata_url, headers=headers)

        if response.status_code is 404:
            log.error("No container with name '%s' is known to Rancher" % container_name)

            return None

        response_json = response.json()

        return [str(port_addr).split(":")[1] for port_addr in response_json]
