"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi import util
from zoomapi.components import base

class ChatChannelsComponentV2(base.BaseComponent):
    """Component dealing with all chat channels related matters"""

    def list(self, **kwargs):
        return self.get_request("/chat/users/me/channels")

    def create_channel(self, **kwargs):
        return self.post_request("/chat/users/me/channels", data = kwargs)

    def get_channel(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.get_request(
            "/chat/channels/{}".format(kwargs.get("channelId")), params = kwargs
        )

    def update_channel(self, **kwargs):
        util.require_keys(kwargs, ["channelId", "name"])
        return self.patch_request(
            "/chat/channels/{}".format(kwargs.get("channelId")), data = kwargs
        )

    def delete_channel(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.delete_request(
            "/chat/channels/{}".format(kwargs.get("channelId")), params = kwargs
        )

    def list_channel_members(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.get_request(
            "/chat/channels/{}/members".format(kwargs.get("channelId")), params = kwargs
        )

    def invite_channel_members(self, **kwargs):
        util.require_keys(kwargs, ["channelId", "members"])
        return self.post_request(
            "/chat/channels/{}/members".format(kwargs.get("channelId")), data = kwargs
        )

    def join_channel(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.post_request(
            "/chat/channels/{}/members/me".format(kwargs.get("channelId")), data = kwargs
        )

    def leave_channel(self, **kwargs):
        util.require_keys(kwargs, "channelId")
        return self.delete_request(
            "/chat/channels/{}/members/me".format(kwargs.get("channelId")), params = kwargs
        )

    def remove_member(self, **kwargs):
        util.require_keys(kwargs, ["channelId", "memberId"])
        return self.delete_request(
            "/chat/channels/{}/members/{}".format(kwargs.get("channelId"), kwargs.get("memberId")), params = kwargs
        )
