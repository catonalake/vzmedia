from aiohttp import web

from hls_master import HLSMasterManifest
from hls_media import HLSMediaManifest

# Class-based views don't currently work with decorators or CORS, so stick with function views
routes = web.RouteTableDef()
headers = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0',
    'Content-Type': 'application/x-mpegURL'
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
    params = request.rel_url.query

    #cag-ex4 - identify which rays (playlists) to return if any were specified 
    rays_to_return = params.getall('ray', [])

    #cag-ex3 capture any errors in call to build Master
    try:
        manifest = HLSMasterManifest(request, asset_id, rays_to_return)
    except Exception as e:
        return web.Response(status=404)

    #cag-ex3 capture any errors in accessing property attribute of returned class 
    try:
        text=manifest.to_string()
    except Exception as e:
        return web.Response(status=404)

    return web.Response(text=text, headers=headers)


@routes.get('/hls/vod/{asset_id}/{ray}.m3u8')
async def media_get(request):
    asset_id = request.match_info.get('asset_id', '')
    ray = request.match_info.get('ray', '')
    #cag-ex3 capture any errors in call to build Media
    try:
        manifest = HLSMediaManifest(request, asset_id, ray)
    except Exception as e:
        return web.Response(status=404)

    try:
        text=manifest.to_string()
    except Exception as e:
        return web.Response(status=404)

    return web.Response(text=text, headers=headers)

