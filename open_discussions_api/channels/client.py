"""Channels API"""
from urllib.parse import quote

from open_discussions_api.base import BaseApi
from open_discussions_api.channels.constants import CHANNEL_ATTRIBUTES, VALID_CHANNEL_TYPES


class EmptyAttributesError(AttributeError):
    """Error for empty attributes"""
    pass


class UnsupportedAttributeError(AttributeError):
    """Error for an unsupported attribute"""
    pass


class InvalidChannelTypeError(AttributeError):
    """Error for invalid channel type"""
    pass


class ChannelsApi(BaseApi):
    """Channels API"""

    def create(self, **channel_params):
        """create a new channel"""
        if not channel_params:
            raise EmptyAttributesError()

        for key in channel_params:
            if key not in CHANNEL_ATTRIBUTES:
                raise UnsupportedAttributeError("Argument '{}' is not a supported field".format(key))

        if channel_params['channel_type'] not in VALID_CHANNEL_TYPES:
            raise InvalidChannelTypeError(
                "Channel type '{}' is not a valid option".format(channel_params['channel_type'])
            )

        return self.session.post(
            self.get_url("/channels/"),
            json=channel_params
        )

    def add_contributor(self, channel_name, username):
        """Add a contributor to a channel"""

        return self.session.post(
            self.get_url("/channels/{channel_name}/contributors/".format(
                channel_name=quote(channel_name),
            )),
            json={"contributor_name": username}
        )

    def remove_contributor(self, channel_name, username):
        """
        Remove a contributor from a channel
        """

        return self.session.delete(
            self.get_url("/channels/{channel_name}/contributors/{username}/".format(
                channel_name=quote(channel_name),
                username=quote(username),
            ))
        )
