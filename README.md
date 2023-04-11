# YouTube Thumbnails Plugin for Pelican

Pelican plugin for YouTube videos.

This Pelican plugin saves the thumbnails of included YouTube videos inside a local file and includes this image with an hyperlink to the YouTube video itself. This may be used to avoid third-party JavaScript and cookies caused by IFrames for YouTube videos.

## Installation

You can easily install this plugin using *pip* straight from a source checkout: `python -m pip install .`

## Usage

Include the plugin by adding it to your `pelicanconf.py` and referencing it inside your source files using

```
.. youtube:: myVideoId
```

inside an own paragraph.
