"""
An implementation of the encoding.com API in Python

:Author: Sean Myers <smyers@americanri.com>

In lieu of a good test suite (coming soon...), a quick example usage for adding media

>>> import fastenc
>>> format_list = list()
>>> format_list.append(fastenc.query.create_format_element(output='fl9', **{'bitrate': '450k', 'size': '0x240', 'audio_codec': 'libfaac'})
... )
>>> format_list.append(fastenc.query.create_format_element(output='fl9', **{'bitrate': '850k', 'size': '0x360', 'audio_codec': 'libfaac'}))
>>> format_list.append(fastenc.query.create_format_element(output='fl9', **{'bitrate': '1500k', 'size': '0x480', 'audio_codec': 'libfaac'}))
>>> a = fastenc.actions.AddMedia(userid, userkey, mediaid, source, notify, format_list)

"""

VERSION = (0, 1)

import actions
import query
from connection import Connection, ConnectionFailed
