# -*- coding: utf-8 -*-

"""Unittests for db Server.
"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time, datetime
import unittest
import threading
import logging
import time
from pkg_resources import iter_entry_points

from janitoo_nosetests.dbserver import JNTTDBServer, JNTTDBServerCommon
from janitoo_nosetests.thread import JNTTThread, JNTTThreadCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC
from janitoo.utils import JanitooNotImplemented, JanitooException
from janitoo.options import JNTOptions
from janitoo_db.server import JNTDBServer

class CommonServer():
    """Test the models
    """
    loglevel = logging.DEBUG
    path = '/tmp/janitoo_test'
    broker_user = 'toto'
    broker_password = 'toto'
    server_class = JNTDBServer
    server_conf = "tests/data/janitoo_db.conf"
    hadds = [HADD%(2218,0)]

    def test_040_server_start_no_error_in_log(self):
        self.wipTest()
        self.start()
        time.sleep(5)
        if self.server_section:
            print("Look for thread %s"%self.server_section)
            thread = self.server.find_thread(self.server_section)
            self.assertNotEqual(thread, None)
            self.assertIsInstance(thread, JNTBusThread)
        self.waitHeartbeatNodes(hadds=self.hadds)
        time.sleep(self.longdelay)
        self.assertNotInLogfile('^ERROR ')
        #~ self.assertInLogfile('Start the server')
        self.assertInLogfile('Connected to broker')
        self.assertInLogfile('Found heartbeats in timeout')
        print("Reload server")
        self.server.reload()
        time.sleep(5)
        self.waitHeartbeatNodes(hadds=self.hadds)
        time.sleep(self.shortdelay)
        self.assertNotInLogfile('^ERROR ')
        #~ self.assertInLogfile('Reload the server')
        print("Reload threads")
        self.server.reload_threads()
        time.sleep(5)
        self.waitHeartbeatNodes(hadds=self.hadds)
        time.sleep(self.shortdelay)
        self.assertNotInLogfile('^ERROR ')

class TestDbSerser(CommonServer, JNTTDBServerCommon, JNTTDBServer):
    """Test the server
    """
    pass
