import os
from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse


router = APIRouter()

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")


@router.get("/fedora.ico")
async def fedora_ico():
    """
    Give the Fedora ICO file
    """
    return FileResponse(os.path.join(frontend_path, "fedora.ico"))


@router.get("/fedora.svg")
async def fedora_svg():
    """
    Give the Fedora SVG file
    """
    return FileResponse(os.path.join(frontend_path, "fedora.svg"))


@router.get("/docs")
async def docs_redirect():
    """
    Give the OpenAPI3 Docs
    """
    return RedirectResponse("/docs")


@router.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    Give the application
    """
    # Serve static assets with proper MIME types
    if full_path.startswith("assets/"):
        asset_path = os.path.join(frontend_path, full_path)
        if os.path.exists(asset_path):
            return FileResponse(asset_path)
        else:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")
    
    # Don't serve SPA for other asset requests
    if full_path.startswith(("imgs/", "api/")):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    
    print(frontend_path)
    return FileResponse(os.path.join(frontend_path, "index.html"))
