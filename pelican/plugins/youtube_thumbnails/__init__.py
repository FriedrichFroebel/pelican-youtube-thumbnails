#!/usr/bin/env python3

# Avoid attribute errors.
# See https://github.com/getpelican/pelican-plugins/issues/929.
from .youtube_thumbnails import register  # noqa: F401
