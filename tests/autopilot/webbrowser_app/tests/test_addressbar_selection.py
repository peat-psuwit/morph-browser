# -*- coding: utf-8 -*-
#
# Copyright 2013 Canonical
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.

from __future__ import absolute_import

import time

from testtools.matchers import Equals, GreaterThan
from autopilot.matchers import Eventually

from webbrowser_app.tests import StartOpenRemotePageTestCaseBase


class TestAddressBarSelection(StartOpenRemotePageTestCaseBase):

    """Test the address bar selection"""

    def test_click_to_select(self):
        self.assert_chrome_eventually_hidden()
        self.main_window.open_toolbar()
        address_bar = self.main_window.get_address_bar()
        self.pointing_device.click_object(address_bar)
        text_field = self.main_window.get_address_bar_text_field()
        self.assertThat(text_field.selectedText,
                        Eventually(Equals(text_field.text)))

    def test_click_on_action_button(self):
        self.assert_chrome_eventually_hidden()
        self.main_window.open_toolbar()
        action_button = self.main_window.get_address_bar_action_button()
        self.pointing_device.click_object(action_button)
        text_field = self.main_window.get_address_bar_text_field()
        self.assertThat(text_field.selectedText, Eventually(Equals("")))

    def test_second_click_deselect_text(self):
        self.assert_chrome_eventually_hidden()
        self.main_window.open_toolbar()
        address_bar = self.main_window.get_address_bar()
        self.pointing_device.click_object(address_bar)
        # avoid double click
        time.sleep(1)
        self.assert_osk_eventually_shown()
        self.pointing_device.click_object(address_bar)
        text_field = self.main_window.get_address_bar_text_field()
        self.assertThat(text_field.selectedText, Eventually(Equals('')))
        self.assertThat(text_field.cursorPosition, Eventually(GreaterThan(0)))

    def test_double_click_select_word(self):
        self.assert_chrome_eventually_hidden()
        self.main_window.open_toolbar()
        address_bar = self.main_window.get_address_bar()
        self.pointing_device.click_object(address_bar)
        self.assert_osk_eventually_shown()
        self.pointing_device.click_object(address_bar)
        # avoid double click
        time.sleep(1)
        # now simulate a double click
        self.pointing_device.click()
        self.pointing_device.click()
        text_field = self.main_window.get_address_bar_text_field()
        self.assertThat(lambda: len(text_field.selectedText),
                        Eventually(GreaterThan(0)))
