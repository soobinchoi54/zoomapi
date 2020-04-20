# THIS FILE WAS CHANGED FROM THE ORIGINAL

"""Zoom.us REST API Python Client -- Report component"""

from zoomapi import util
from zoomapi.components import base

class ReportComponent(base.BaseComponent):
    """Component dealing with all report related matters"""

    def get_account_report(self, **kwargs):
        util.require_keys(kwargs, ["start_time", "end_time"], kwargs)
        kwargs["from"] = util.date_to_str(kwargs["start_time"])
        del kwargs["start_time"]
        kwargs["to"] = util.date_to_str(kwargs["end_time"])
        del kwargs["end_time"]
        return self.post_request("/report/getaccountreport", params=kwargs)

    def get_user_report(self, **kwargs):
        util.require_keys(kwargs, ["start_time", "end_time"], kwargs)
        kwargs["from"] = util.date_to_str(kwargs["start_time"])
        del kwargs["start_time"]
        kwargs["to"] = util.date_to_str(kwargs["end_time"])
        del kwargs["end_time"]
        return self.post_request("/report/getuserreport", params=kwargs)


class ReportComponentV2(base.BaseComponent):
    def get_user_report(self, **kwargs):
        util.require_keys(kwargs, ["user_id", "start_time", "end_time"])
        kwargs["from"] = util.date_to_str(kwargs["start_time"])
        del kwargs["start_time"]
        kwargs["to"] = util.date_to_str(kwargs["end_time"])
        del kwargs["end_time"]
        return self.get_request(
            "/report/users/{}/meetings".format(kwargs.get("user_id")), params=kwargs
        )

    def get_account_report(self, **kwargs):
        util.require_keys(kwargs, ["start_time", "end_time"])
        kwargs["from"] = util.date_to_str(kwargs["start_time"])
        del kwargs["start_time"]
        kwargs["to"] = util.date_to_str(kwargs["end_time"])
        del kwargs["end_time"]
        return self.get_request("/report/users", params=kwargs)
