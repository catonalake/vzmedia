import urllib.parse

from data import ASSETS
from templates import hls_master_head, hls_master_ray, hls_master_ifo_ray


class HLSMasterManifest:
    def __init__(self, request, asset_id):
        """
        Used to create an HLS master manifest for an asset record. Endpoints will
        typically only use the to_string function.

        :param request: Request object from the web server
        :param request: the GUID for an asset whose master playlist we want to generate
        """
        self.request = request
        self.doc = ASSETS[asset_id]
        self.doc.update({'hls_version': 4})

    def to_string(self):
        """
        Take the list from "assemble" and put it into a single text string to
        send to the client
        """
        return "\n".join(self.assemble())

    def assemble(self):
        """
        Build a list where each item is a string representing one line of the
        manifest
        """
        # header
        content = [hls_master_head.format(**self.doc)]

        # variant streams
        scheme = self.request.scheme
        netloc = self.request.host
        for ray_name, ray_data in self.doc['rays'].items():
            content.append(hls_master_ray.format(**ray_data))
            path = 'hls/vod/{}/{}.m3u8'.format(self.doc['_id'], ray_name)
            qs = ''
            url = urllib.parse.urlunparse((scheme, netloc, path, None, qs, None))
            content.append(url)

        return content
