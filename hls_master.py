import urllib.parse

from data import ASSETS
from templates import hls_master_head, hls_master_ray, hls_master_sub


class HLSMasterManifest:
    def __init__(self, request, asset_id, rays_to_return):
        """
        Used to create an HLS master manifest for an asset record. Endpoints will
        typically only use the to_string function.

        :param request: Request object from the web server
        :param request: the GUID for an asset whose master playlist we want to generate
        :param rays_to_return: an array of rays to return or an empty array to return all
        """
        self.request = request
        self.asset_id = asset_id
        self.rays_to_return = rays_to_return
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
        rays_provided = len(self.rays_to_return) > 0
        for ray_name, ray_data in self.doc['rays'].items():
            # build only if the ray is on our list or if no rays were explicity specified
            if not rays_provided or ray_name in self.rays_to_return:
                content.append(self.url_generator(ray_data, hls_master_ray, ray_name, content))

        #cag-ex4 subtitles
        if 'subtitles' in self.doc:
            for sub_name, sub_data in self.doc['subtitles'].items():
                content.append(self.url_generator(sub_data, hls_master_sub, sub_name, content))
        return content

    def url_generator(self, dict_data, template_string, dict_name, content):
        """
        Build a url using a common pattern with differing variables
        """
        scheme = self.request.scheme
        netloc = self.request.host

        content.append(template_string.format(**dict_data))
        path = 'hls/vod/{}/{}.m3u8'.format(self.doc['_id'], dict_name)
        qs = ''
        url = urllib.parse.urlunparse((scheme, netloc, path, None, qs, None))
        return(url)
