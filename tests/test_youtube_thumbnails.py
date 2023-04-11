#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import mock, TestCase

from pelican.contents import Static
from pelican.readers import Readers
from pelican.tests.support import get_settings

from pelican.plugins.youtube_thumbnails import youtube_thumbnails


# Disable verbose logging of `pelican`.
logging.getLogger().setLevel(logging.WARNING)


class YoutubeThumbnailsPluginTestCase(TestCase):
    @property
    def test_data(self) -> Path:
        return Path(__file__).resolve().parent / "test_data"

    def test_get_output_file(self):
        with TemporaryDirectory() as directory:
            directory = Path(directory)
            shutil.rmtree(directory)

            settings = dict(OUTPUT_PATH=str(directory))

            path = youtube_thumbnails.get_output_file(
                settings=settings, video_id="1337"
            )
            self.assertFalse(path.exists(), path)
            self.assertTrue(path.parent.is_dir(), path)

            path = youtube_thumbnails.get_output_file(settings=settings, video_id="42")
            self.assertFalse(path.exists(), path)
            self.assertTrue(path.parent.is_dir(), path)

    def test_get_logo_file(self):
        with youtube_thumbnails.get_logo_file() as path:
            self.assertTrue(path.is_file(), path)
            content = path.read_bytes()
        self.assertEqual(
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00P\x00\x00\x008\x08\x06\x00\x00\x00j\xb6\x7f\x9a\x00\x00\x00\tpHYs\x00\x00\x0b\x12\x00\x00\x0b\x12\x01\xd2\xdd~\xfc\x00\x00\x023IDATx\xda\xed\x9c\xdbq\x830\x10E\xaf2\xf9\x8f:\x08\x1d\x84\x0eB\t\x94\x90\x12H\x07\xee \xb8\x83\x94`w@:P: \x1d\xc8\x15l>,%6/\x03\xc6\x11\x90{f4\xf6`\x7f\x98c!v\x17\x16%"\x98\x1c\xa5"\x00\xd1\xc9\x96\x18\x80\xae|K\xbb\xedS`\x00\xd8\xca6\xeb\xb6{J\x88\x94\x93\xef\xea(\x81J\xc5N\x90\x7f\x8d\x9c\x90\',\x83O\'\xb8t\xc38\xc1\xe66\x02\x8f\xc2^\x9c\xb0g\xac\x9b\x0f\'\xf4\xbd\x97P\x11i\x1f@"\x80\x11@\xfe\xe90\x02$]\x8e\xba\xe4m\xfe\xb1\xb8\xea\xd8\x0c\x13\x08\xe4\x94V\x1by?\x81@JY\xad#\xad\xfa:?\x89(\xa5\xdd\x02\xfa\x08\xd2\xc4\x17\x80\x18"?!\xd3]\xe5\x0b)\xe5u\xf2\xe8\x1c\xa1K \xe9&m\x8f\x03\x95\x12\xfa\xe9\x81\x88\xaa\xcf\xc0c\xb0L\xfagb\xb5CX\xd3Lot\x93\xc0\x84^z\x93\xb4\x9dD\xc8@\xc2\xcf@\xad9\x03\xaf\xa2,\x81,[\xc5\x0c\x0c\xc3\xc3\x03\xf0\xf6\x06\x18\x03$\x0b\\\x86Or`\x1b$\xbf\xac\xb2\xdb\x89D\xd1\xdcsb[/&\x84\xfa1MX+\xb2\xd9\x88h=_\x89\xb3\x16\xe8)K\x914\xa5\xc0\xd1\x02=E!\x12\xc7\x148Z\xa0\'\xcf\xe7sX/R\xa0_\x1f\xb3\x8c\x02G\x0b\xf4\x18#\x92$\x14x5\xa1\xc2\x9e3\x81@\xb4X\x81\xa1\xc2\x9e\xd5\xcc\xc0Pa\x8f\xf3\xc6j\xcc\x95\xdc\xafb/\x0e\x07 \xcf\x8f\xc3\xda`\xb90O"\x0cc(\x90\x814S9\x16\x13X\xce\xa2\xc0\x85\x16TY\xd2\xbf\xb2\xa4_\x04\x15\x18:,\x196\x8a\xf9\xa4r\x87\x03\xf0\xfa\n\xc41P\x14L\xe5\x06\x13E\x7f\x9f~\xdd\xe8\xbap\x98\xbf\x7f\x99\xf2\n\xde\x1b\xb3\x9a\x19\xb8L\x1ag\xa0\xa5\x97\xfe\x0b\x8f\x7f\xc3[|\xc7\xd5\x00U\xdb\x1a\xb8\xa7\x9d\x8b\xec\xbb\xee\xce\xda\xd1\xcfE\xce\x1c\xb1\xd1f\x18\x17\x1am\x8e\x1fd\xf4\xd4Jv*\xaf9\x0e\x14\xd9\x01\xd8\xd2U\x8d\xads\xd3rQ\x89\xed\xae\x13\xb6\xbb\xb2\xe1\xfa\xb7\xear\xa1\xe1\x9a-\xffu\x06\xb5\xfc\xf3\xa1\x13\x7f\xf2\xd0\x89\xe1\x82\xbdTO\xd3cO\x80\xe9zS\x8a\x96t\xeb\xe6\x8f=\xf9\x06.\x9bK;B\x88}n\x00\x00\x00\x00IEND\xaeB`\x82',  # noqa: E501
            content,
        )

    def test_add_image_overlay(self):
        # https://pixabay.com/de/illustrations/blau-kristall-w%c3%bcrfel-tief-5457731/
        path = self.test_data / "image_240p.png"
        result = youtube_thumbnails.add_image_overlay(path.read_bytes())
        expected = self.test_data / "image_240p_with_overlay.png"

        with NamedTemporaryFile(suffix=".png") as actual:
            result.save(actual.name)
            self.assertEqual(expected.read_bytes(), Path(actual.name).read_bytes())

    def test_save_thumbnail__with_overlay(self):
        path = mock.MagicMock()
        path.exists.return_value = True
        settings = dict(YOUTUBE_ADD_OVERLAY=True)

        with mock.patch.object(youtube_thumbnails.requests, "get") as get_mock:
            # File already exists.
            youtube_thumbnails.save_thumbnail(
                settings=settings, video_id="42", output_file=path
            )
            get_mock.assert_not_called()

            # Actual saving.
            path.exists.return_value = False
            image = mock.MagicMock()
            response = mock.MagicMock()
            content = object()
            response.content = content
            get_mock.return_value = response
            with mock.patch.object(
                youtube_thumbnails, "add_image_overlay", return_value=image
            ) as add_mock, mock.patch.object(
                image, "save"
            ) as save_mock, mock.patch.object(
                image, "close"
            ) as close_mock:
                youtube_thumbnails.save_thumbnail(
                    settings=settings, video_id="42", output_file=path
                )
                get_mock.assert_called_once_with(
                    "https://i.ytimg.com/vi/42/maxresdefault.jpg"
                )
                add_mock.assert_called_once_with(content)
                save_mock.assert_called_once_with(path)
                close_mock.assert_called_once_with()

    def test_save_thumbnail__without_overlay(self):
        path = mock.MagicMock()
        path.exists.return_value = False
        settings = dict(YOUTUBE_ADD_OVERLAY=False)

        with mock.patch.object(youtube_thumbnails.requests, "get") as get_mock:
            image = mock.MagicMock()
            response = mock.MagicMock()
            content = object()
            response.content = content
            get_mock.return_value = response
            with mock.patch.object(
                youtube_thumbnails, "add_image_overlay", return_value=image
            ) as add_mock, mock.patch.object(
                image, "save"
            ) as save_mock, mock.patch.object(
                image, "close"
            ) as close_mock, mock.patch.object(
                path, "write_bytes"
            ) as write_mock:
                youtube_thumbnails.save_thumbnail(
                    settings=settings, video_id="42", output_file=path
                )
                get_mock.assert_called_once_with(
                    "https://i.ytimg.com/vi/42/maxresdefault.jpg"
                )
                add_mock.assert_not_called()
                save_mock.assert_not_called()
                close_mock.assert_not_called()
                write_mock.assert_called_once_with(content)

    def test_create_html_for_image(self):
        settings = dict(SITEURL="https://example.org/blog/")
        result = youtube_thumbnails.create_html_for_image(
            settings=settings, video_id="42"
        )
        self.assertEqual(
            (
                '<a href="https://youtube.com/embed/42" target="_blank">'
                '<img src="https://example.org/blog//images/youtube/42.jpg"></a>'
            ),
            result,
        )

    def _get_html_page_from_markdown(self, markdown):
        with NamedTemporaryFile(suffix=".md") as path:
            path = Path(path.name)
            path.write_text(markdown)
            result = Readers(get_settings(filenames=dict())).read_file(
                base_path=path.parent, path=path.name
            )
        return result

    def test_replace_youtube(self):
        page = self._get_html_page_from_markdown(
            """
            title: My page

### My page

Welcome to my page!

.. note::

   See other pages as well.

Want to learn more? Have a look at the video:

.. youtube:: 1337

.. youtube:: 1338

Unrelated text.

.. youtube:: qwertz1234
            """
        )
        old_content = page._content

        with mock.patch.object(
            youtube_thumbnails, "get_output_file"
        ) as get_mock, mock.patch.object(
            youtube_thumbnails, "save_thumbnail"
        ) as save_mock:
            youtube_thumbnails.replace_youtube(page)
        get_mock.assert_has_calls(
            [
                mock.call(settings=page.settings, video_id=video_id)
                for video_id in ["1337", "1338", "qwertz1234"]
            ],
            any_order=True,
        )
        self.assertEqual(3, get_mock.call_count, get_mock.call_args_list)
        self.assertEqual(3, save_mock.call_count, save_mock.call_args_list)

        new_content = page._content
        self.assertNotEqual(old_content, new_content)

        self.assertIn(
            (
                '<p><a href="https://youtube.com/embed/1337" target="_blank"><img src="/images/youtube/1337.jpg"></a></p>\n'
                '<p><a href="https://youtube.com/embed/1338" target="_blank"><img src="/images/youtube/1338.jpg"></a></p>\n'
                "<p>Unrelated text.</p>\n"
                '<p><a href="https://youtube.com/embed/qwertz1234" target="_blank"><img src="/images/youtube/qwertz1234.jpg"></a></p>'
            ),
            new_content,
        )

    def test_replace_youtube__additional_values(self):
        page = self._get_html_page_from_markdown(
            """
.. youtube:: 1337
   key: value
   Some text
"""
        )
        with mock.patch.object(
            youtube_thumbnails, "get_output_file"
        ) as get_mock, mock.patch.object(
            youtube_thumbnails, "save_thumbnail"
        ) as save_mock:
            with self.assertRaisesRegex(
                expected_exception=youtube_thumbnails.UnsupportedMetadata,
                expected_regex=r"^\'   key: value\\n   Some text\'$",
            ):
                youtube_thumbnails.replace_youtube(page)
        get_mock.assert_not_called()
        save_mock.assert_not_called()

    def test_replace_youtube__static(self):
        with mock.patch.object(youtube_thumbnails, "BeautifulSoup") as soup_mock:
            static = Static(content=b"1234567890")
            youtube_thumbnails.replace_youtube(static)
            soup_mock.assert_not_called()
