import aiohttp_cors
from aiohttp import web

from aioweb.views import routes

app = web.Application()
app.router.add_routes(routes)

# Configure CORS on all routes.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        expose_headers="*", allow_headers="*",
    )
})
for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app)

