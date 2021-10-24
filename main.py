#! /usr/bin/env python

from aiohttp.web import run_app
from app import create_app

if __name__ == '__main__':
    app = create_app()
    run_app(app)
