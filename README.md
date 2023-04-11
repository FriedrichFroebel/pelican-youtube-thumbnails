# YouTube Thumbnails Plugin for Pelican

Pelican plugin for YouTube videos.

This Pelican plugin saves the thumbnails of included YouTube videos inside a local file and includes this image with an hyperlink to the YouTube video itself. This may be used to avoid third-party JavaScript and cookies caused by IFrames for YouTube videos.

## Installation

The package is available on PyPI and can be installed using `pip install pelican-youtube-thumbnails`.

Alternatively, you may want to install it straight from a source checkout: `python -m pip install .`

## Usage

Include the plugin by adding it to your `pelicanconf.py` and referencing it inside your source files using

```
.. youtube:: myVideoId
```

inside an own paragraph.
