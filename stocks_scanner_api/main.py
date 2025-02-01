"""
Main application entry point.
"""

from fastapi import FastAPI
from app.config import API_TITLE, API_DESCRIPTION, API_VERSION
from app.api import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION
    )

    # Add routes
    app.include_router(router)

    @app.get("/")
    async def root():
        """Root endpoint returning API information."""
        return {
            "name": API_TITLE,
            "version": API_VERSION,
            "endpoints": [
                "/sec-filings/{ticker}"
            ]
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
