#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

import codecs
import functools
import json
import re
from typing import List

import bugzilla
import reviewboard

irc_channel = '#reviewbot' # This is for debug purposes.

def get_review_request_url(message: dict) -> str:
    """Return the review request url associated with the message."""
    review_request_id = get_review_request_id(message)
    return reviewboard.build_review_request_url(
            message['payload']['review_board_url'], review_request_id)

def get_review_request_id(message: dict) -> int:
    """Return the review request id associated with the message."""
    if message['_meta']['routing_key'] == 'mozreview.commits.published':
        return message['payload']['parent_review_request_id']
    elif message['_meta']['routing_key'] == 'mozreview.review.published':
        return message['payload']['review_request_id']

async def generate_content_text(id: int) -> str:
    """Generate an actionable text for reviews."""
    status = await reviewboard.get_review_request_status(id)
    if status == True:
        return 'r+ was granted'
    return '{} issues left'.format(status)

def get_requester(message: dict) -> str:
    return message['payload']['review_request_submitter']

async def get_reviewers(id: int) -> List[str]:
    return await reviewboard.get_reviewers_from_id(id)

async def get_bugzilla_components_from_msg(msg: dict) -> List[str]:
    """Get the bugzilla component that relates to the bug the review is for."""
    if msg['_meta']['routing_key'] == 'mozreview.review.published':
        bz_comps = set()
        for bug_id in msg['payload']['review_request_bugs']:
            bz_comp = await bugzilla.get_bugzilla_component(bug_id)
            bz_comps.add(bz_comp)
        return list(bz_comps)
    if msg['_meta']['routing_key'] == 'mozreview.commits.published':
        bug_ids = await reviewboard.get_bugzilla_ids(get_review_request_id(msg))
        bz_comps = []
        for bug in bug_ids:
            bz_comps.append(await bugzilla.get_bugzilla_component(bug))

        return bz_comps