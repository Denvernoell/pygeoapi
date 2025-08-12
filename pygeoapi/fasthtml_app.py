# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2020 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

"""FastHTML module providing the route paths to the api"""

import logging
import os
import sys
from typing import Union

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not installed. Using system environment variables only.")
    pass

# Add the current directory to Python path to find pygeoapi modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fasthtml.common import *
    from starlette.requests import Request
    from starlette.responses import Response, JSONResponse, PlainTextResponse
    from starlette.middleware.cors import CORSMiddleware
except ImportError:
    print("FastHTML not installed. Install with: pip install python-fasthtml")
    sys.exit(1)

from pygeoapi.api import API, APIRequest
from pygeoapi.api import (
    landing_page as api_landing_page,
    openapi_ as api_openapi,
    conformance as api_conformance,
    describe_collections as api_collections
)
import pygeoapi.api.itemtypes as itemtypes_api
from pygeoapi.config import get_config
from pygeoapi.openapi import load_openapi_document
from pygeoapi.util import get_api_rules, to_json, format_datetime

LOGGER = logging.getLogger(__name__)

# Load configuration
CONFIG = get_config()

# Create API instance (this will generate OpenAPI document on the fly)
try:
    from pygeoapi.openapi import get_oas
    OPENAPI = get_oas(CONFIG)
    api_ = API(CONFIG, OPENAPI)
except Exception as e:
    LOGGER.error(f"Failed to load OpenAPI document: {e}")
    # Fallback: create basic API without OpenAPI
    api_ = API(CONFIG, {})

API_RULES = get_api_rules(CONFIG)

# FastHTML app instance
try:
    TLINK = Script(src="https://unpkg.com/tailwindcss@3/lib/index.js")
    APP, RT = fast_app(
        live=True,
        debug=True,
        hdrs=(TLINK,)
    )
except NameError:
    # Fallback if FastHTML components aren't available
    from starlette.applications import Starlette
    from starlette.routing import Route
    APP = Starlette(debug=True)
    
    # Simple route decorator for fallback
    def RT(path):
        def decorator(func):
            APP.router.routes.append(Route(path, func, methods=["GET", "POST"]))
            return func
        return decorator

# Add CORS middleware
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get static folder
STATIC_FOLDER = 'static'
if 'templates' in CONFIG['server']:
    STATIC_FOLDER = CONFIG['server']['templates'].get('static', 'static')

# API instance
api_ = API(CONFIG, OPENAPI)

def get_response(
    result: dict,
    response_type: str,
    status_code: int = 200
) -> Response:
    """
    Prepare response object for FastHTML
    
    :param result: API result dictionary
    :param response_type: response content type
    :param status_code: HTTP status code
    
    :returns: FastHTML/Starlette Response object
    """
    
    if response_type == 'application/json':
        if isinstance(result, dict):
            result = to_json(result)
        return JSONResponse(
            content=result,
            status_code=status_code,
            headers={'Content-Type': 'application/json'}
        )
    
    elif response_type == 'text/plain':
        return PlainTextResponse(
            content=str(result),
            status_code=status_code
        )
    
    elif response_type == 'text/html':
        # For HTML responses, use FastHTML components
        if isinstance(result, dict):
            return JSONResponse(content=result, status_code=status_code)
        return Response(
            content=str(result),
            status_code=status_code,
            media_type="text/html"
        )
    
    else:
        return Response(
            content=str(result),
            status_code=status_code,
            media_type=response_type
        )

async def execute_from_fasthtml(api_function, request: Request, *args, **kwargs):
    """
    Executes API function from FastHTML request
    
    :param api_function: function to execute
    :param request: FastHTML/Starlette request object
    :param args: function arguments
    :param kwargs: function keyword arguments
    
    :returns: HTTP response
    """
    
    try:
        # Convert Starlette request to APIRequest (async)
        api_request = await APIRequest.from_starlette(request, api_.locales)
        
        # Execute the API function
        headers, status_code, content = api_function(api_, api_request, *args, **kwargs)
        
        # Determine response type from headers
        response_type = headers.get('Content-Type', 'application/json')
        
        return get_response(content, response_type, status_code)
        
    except Exception as err:
        LOGGER.exception(err)
        return JSONResponse(
            content={'error': str(err)},
            status_code=500
        )

# Route definitions
@RT("/")
async def landing_page(request: Request):
    """Landing page route"""
    return await execute_from_fasthtml(api_landing_page, request)

@RT("/openapi")
async def openapi_spec(request: Request):
    """OpenAPI specification route"""
    return await execute_from_fasthtml(api_openapi, request)

@RT("/conformance")
async def conformance(request: Request):
    """Conformance route"""
    return await execute_from_fasthtml(api_conformance, request)

@RT("/collections")
async def collections(request: Request):
    """Collections route"""
    return await execute_from_fasthtml(api_collections, request)

@RT("/collections/{collection_id}")
async def collection_by_id(request: Request, collection_id: str):
    """Specific collection route"""
    return await execute_from_fasthtml(api_collections, request, collection_id)

@RT("/collections/{collection_id}/items")
async def collection_items(request: Request, collection_id: str):
    """Collection items route"""
    return await execute_from_fasthtml(itemtypes_api.get_collection_items, request, collection_id)

@RT("/collections/{collection_id}/items/{item_id}")
async def collection_item_by_id(request: Request, collection_id: str, item_id: str):
    """Specific collection item route"""
    return await execute_from_fasthtml(itemtypes_api.get_collection_item, request, collection_id, item_id)

# Static files
@RT("/static/{filepath:path}")
def static_files(filepath: str):
    """Serve static files"""
    try:
        from starlette.responses import FileResponse
        return FileResponse(os.path.join(STATIC_FOLDER, filepath))
    except ImportError:
        return Response("Static files not available", status_code=404)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(APP, host="0.0.0.0", port=5000, reload=True)
