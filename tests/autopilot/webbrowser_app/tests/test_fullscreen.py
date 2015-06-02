# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright 2014-2015 Canonical
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from webbrowser_app.tests import StartOpenRemotePageTestCaseBase

from testtools.matchers import Equals, LessThan
from autopilot.matchers import Eventually
from autopilot.platform import model


class TestFullscreen(StartOpenRemotePageTestCaseBase):

    # Ref: http://doc.qt.io/qt-5/qwindow.html#Visibility-enum
    QWINDOW_FULLSCREEN = 5

    def setUp(self):
        self.url = self.base_url + "/fullscreen"
        super(TestFullscreen, self).setUp()

    def assert_eventually_windowed(self):
        self.assertThat(self.main_window.get_current_webview().fullscreen,
                        Eventually(Equals(False)))
        self.assertThat(self.main_window.get_window().visibility,
                        Eventually(LessThan(self.QWINDOW_FULLSCREEN)))

    def assert_eventually_fullscreen(self):
        self.assertThat(self.main_window.get_current_webview().fullscreen,
                        Eventually(Equals(True)))
        self.assertThat(self.main_window.get_window().visibility,
                        Eventually(Equals(self.QWINDOW_FULLSCREEN)))

    def test_toggle_fullscreen(self):
        self.assert_eventually_windowed()
        webview = self.main_window.get_current_webview()
        self.pointing_device.click_object(webview)
        self.assert_eventually_fullscreen()
        hint = webview.wait_select_single(objectName="fullscreenExitHint")
        self.pointing_device.click_object(webview)
        self.assert_eventually_windowed()
        hint.wait_until_destroyed()

    def test_exit_fullscreen(self):
        webview = self.main_window.get_current_webview()
        self.pointing_device.click_object(webview)
        self.assert_eventually_fullscreen()
        if model() == 'Desktop':
            self.keyboard.press_and_release('Escape')
        else:
            self.open_tabs_view()
        self.assert_eventually_windowed()
