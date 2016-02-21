# -*- coding: utf-8 -*-

"""Unittests for models.
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
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time, datetime
import unittest
import threading
import logging
from pkg_resources import iter_entry_points

from sqlalchemy.orm import sessionmaker, scoped_session

from janitoo_nosetests import JNTTBase
from janitoo_nosetests.models import JNTTModels

from janitoo.options import JNTOptions
from janitoo_db.base import Base, create_db_engine
from janitoo_db.migrate import Config as JNTConfig
import janitoo_db.models as jntmodels

class CommonModels(object):
    """Test the dbman
    """

    def test_101_versiondb(self):
        config = JNTConfig(conf_file=self.models_conf)
        config.initdb()
        versions = config.versiondb()
        self.assertTrue(len(versions)>0)

    def test_111_heads(self):
        config = JNTConfig(conf_file=self.models_conf)
        heads = config.heads()
        self.assertTrue(len(heads)>0)

    def test_121_checkdb(self):
        config = JNTConfig(conf_file=self.models_conf)
        config.initdb()
        self.assertTrue(config.checkdb())
        config.downgrade()
        self.assertFalse(config.checkdb())

class TestMigrateSQLite(JNTTBase, CommonModels):
    """Test the models
    """
    models_conf = "tests/data/janitoo_db.conf"

class TestMigrateMySQL(JNTTBase, CommonModels):
    """Test the models
    """
    models_conf = "tests/data/janitoo_db_mysql.conf"

class TestMigratePostgresql(JNTTBase, CommonModels):
    """Test the models
    """
    models_conf = "tests/data/janitoo_db_postgres.conf"

