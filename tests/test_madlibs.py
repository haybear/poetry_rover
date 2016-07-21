#!/usr/bin/env python3

# Copyright (C) 2016 Haybear
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import unittest.mock as mock

import madlibs


ORIGINAL_TEXT = """These weapons are coupled to a computerised day/night fire control system that allows stationary and moving targets to be engaged with a high first-round hit probability while the vehicle is moving."""  # NOQA

MADLIBS_TEXT = """These weapons {verb} a computerized {noun} fire control system that {verb} stationary and moving {noun} to be {verb} with a high first round hit probability while the vehicle is {verb}."""  # NOQA

FINAL_TEXT = """These weapons burn a computerized whiff fire control system that shrivels stationary and moving tempests to be fried with a high first round hit probability while the vehicle is blasting."""  # NOQA


class MadlibsTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_verb = mock.MagicMock()
        self.mock_noun = mock.MagicMock()

    def test_substitute(self):
        self.mock_verb.__str__ = mock.Mock(
            side_effect=['burn', 'shrivels', 'fried', 'blasting'])
        self.mock_noun.__str__ = mock.Mock(
            side_effect=['whiff', 'tempests'])
        result = madlibs.substitute(
            MADLIBS_TEXT, self.mock_noun, self.mock_verb)
        self.assertEqual(FINAL_TEXT, result)
