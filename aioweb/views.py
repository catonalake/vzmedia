from aiohttp import web

from hls_master import HLSMasterManifest
from hls_media import HLSMedia

# Class-based views don't currently work with decorators or CORS, so stick with function views
routes = web.RouteTableDef()
headers = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0',
}


@routes.get('/')
async def home(request):
    return web.Response(text="no content")


@routes.get('/test')
async def test(request):  # pragma: no cover
    return web.Response(text="Test complete")


@routes.get('/hls/vod/{asset_id}.m3u8')
async def master_get(request):
    asset_id = request.match_info.get('asset_id', '')
    manifest = HLSMasterManifest(request, asset_id)
    return web.Response(text=manifest.to_string(), headers=headers)


@routes.get('/hls/vod/{asset_id}/{ray}.m3u8')
async def media_get(request):
    asset_id = request.match_info.get('asset_id', '')
    ray = request.match_info.get('ray', '')
    manifest = HLSMedia(request, asset_id, ray)
    return web.Response(text=manifest.to_string(), headers=headers)

