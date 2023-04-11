#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pelican plugin for YouTube videos.

This Pelican plugin saves the thumbnails of included YouTube videos inside a
local file and includes this image with an hyperlink to the YouTube video
itself. This may be used to avoid third-party JavaScript and cookies caused by
IFrames for YouTube videos.

Include the plugin by adding it to your `pelicanconf.py` and referencing it
inside your source files using :code:`.. youtube:: myVideoId` inside an own
paragraph.
"""

import sys
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, NoReturn

import requests
from PIL import Image
from bs4 import BeautifulSoup
from pelican.plugins import signals
from pelican.contents import Content, Static

if sys.version_info < (3, 9):
    import importlib_resources  # noqa: F401
else:
    import importlib.resources as importlib_resources  # noqa: F401


PELICAN_SETTINGS_TYPE = Dict[str, Any]


def get_output_file(settings: PELICAN_SETTINGS_TYPE, video_id: str) -> Path:
    """
    Get the path to the output file. Silently creates the output directory in
    the background, too.

    :param settings: The settings to get the output directory from.
    :param video_id: The ID of the YouTube video.
    :return: The path for the output file.
    """
    directory = Path(settings.get("OUTPUT_PATH"), "images", "youtube")
    if not directory.exists():
        directory.mkdir(parents=True)

    return directory / f"{video_id}.jpg"


@contextmanager
def get_logo_file() -> Path:
    """
    Get the path to the YouTube logo file.

    :return: The path to the logo.
    """
    path = importlib_resources.files("pelican.plugins.youtube_thumbnails") / "logo.png"
    with importlib_resources.as_file(path) as path:
        yield path


def add_image_overlay(image_content: bytes) -> Image.Image:
    """
    Add a YouTube play button overlay in the center of the given image.

    :param image_content: The image to add the overlay to.
    :return: The given image with the YouTube overlay.
    """
    image = Image.open(BytesIO(image_content))
    with get_logo_file() as logo_file:
        overlay = Image.open(logo_file)

        # Get the image sizes for the offset calculation.
        image_width, image_height = image.size
        overlay_width, overlay_height = overlay.size

        # Calculate the offset to place the overlay in the center.
        offset = (
            (image_width - overlay_width) // 2,
            (image_height - overlay_height) // 2,
        )

        # Add the overlay and return the image.
        # If we do not add the `mask` parameter, the transparent background of the
        # overlay would get ignored which results in ugly output.
        image.paste(overlay, offset, mask=overlay)
        overlay.close()
    return image


def save_thumbnail(
    settings: PELICAN_SETTINGS_TYPE, video_id: str, output_file: Path
) -> NoReturn:
    """
    Save the thumbnail of the given video inside the specified file. This may
    add an overlay to the thumbnail itself.

    :param settings: The Pelican settings to use.
    :param video_id: The ID of the YouTube video.
    :param output_file: The output file to use.
    """
    # Do not recreate existing images in every run. Use `pass` instead of
    # `return` for tests during development.
    if output_file.exists():
        return

    # Download the thumbnail with the best resolution.
    url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    response_content = requests.get(url).content

    # Get the output image and save it.
    if settings.get("YOUTUBE_ADD_OVERLAY", True):
        output_image = add_image_overlay(response_content)
        output_image.save(output_file)
        output_image.close()
    else:
        output_file.write_bytes(response_content)


def create_html_for_image(settings: PELICAN_SETTINGS_TYPE, video_id: str) -> str:
    """
    Create the HTML code for the image link.

    :param settings: The settings to get the site URL from.
    :param video_id: The ID of the YouTube video.
    :return: The HTML to include into the page.
    """
    return (
        f'<a href="https://youtube.com/embed/{video_id}" target="_blank">'
        f'<img src="{settings.get("SITEURL")}/images/youtube/{video_id}.jpg"></a>'
    )


class UnsupportedMetadata(ValueError):
    pass


def replace_youtube(content: Content):
    """
    The main method to replace the YouTube directive used inside the source
    files with the right representation.

    :param content: The content object to get the needed data from.
    """
    # We do not want to process static files.
    if isinstance(content, Static):
        return

    # Convert the content HTML string to a usable object.
    html = BeautifulSoup(content._content, "lxml")

    # Iterate over all paragraphs to search for YouTube directives.
    for paragraph in html.find_all("p"):
        text = paragraph.get_text()

        # Skip paragraphs without the YouTube directive.
        if not text.startswith(".. youtube::"):
            continue

        # Extract the video ID, save the image and prepare the HTML code to
        # insert.
        video_id = text.split("::")[1].strip()
        if "\n" in video_id:
            raise UnsupportedMetadata(repr(video_id.split("\n", maxsplit=1)[1]))
        file_path = get_output_file(settings=content.settings, video_id=video_id)
        save_thumbnail(
            settings=content.settings, video_id=video_id, output_file=file_path
        )
        html_img = create_html_for_image(settings=content.settings, video_id=video_id)

        # Replace the old text with our new code. This seems to be the only
        # working way to change the output DOM.
        # Access to private attributes intended, see
        # https://github.com/getpelican/pelican/issues/1921.
        content._content = content._content.replace(text, html_img)


def register():
    """
    Register the plugin action to be performed after processing the source file
    and before writing the HTML output. This method is required by Pelican for
    every plugin.
    """
    signals.content_object_init.connect(replace_youtube)
