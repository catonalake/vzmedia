from random import choice
from urllib.parse import urlunparse

from data import ASSETS
from templates import hls_media_head


class HLSMedia:
    def __init__(self, request, asset_id, ray):
        """
        Used to create an HLS media playlist for an asset record. Endpoints will
        typically only use the to_string function.

        :param request: Request object from the web server
        :param ray: The ray we're building a media playlist for
        """
        self.request = request
        self.doc = ASSETS[asset_id]
        self.doc.update({'hls_version': 4})
        self.ray = ray

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

        # Header
        content = [hls_media_head.format(**self.doc)]

        # Segment list
        segment_count = 0
        segment_url_template = self.doc.get('segment_url_template')
        for range in self.doc.get('range_durations'):
            for segment_duration in range:
                content.append(self.make_key_line(self.doc.get('_id'), self.ray, segment_count))
                content.append("#EXTINF:{},".format(segment_duration))
                content.append(segment_url_template.format(**{
                    'prefix': self.ray.upper(),
                    'segment_number': segment_count})
                               )
                segment_count += 1


        # end the playlist
        content.append("#EXT-X-ENDLIST")
        return content

    def make_key_line(self, beam_id, ray, segment_count=0):
        scheme = 'https'
        netloc = 'content.downlynk.com'
        path = '/check2?b={beam_id}&v={beam_id}&r={ray}'.format(
            **{'beam_id': beam_id,
               'ray': ray})
        key_url = urlunparse((scheme, netloc, path, None, None, None))

        method = 'AES-128'
        key_line = '#EXT-X-KEY:METHOD={},URI="{}",IV=0x{:032X}'.format(method, key_url, segment_count)
        # key_line = '#EXT-X-KEY:METHOD={},URI="{}"'.format(method, key_url, segment_count)
        return key_line
