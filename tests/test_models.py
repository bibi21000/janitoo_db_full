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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time, datetime
import unittest
import threading
import logging
import pkg_resources

from sqlalchemy.orm import sessionmaker, scoped_session

from janitoo_nosetests import JNTTBase
from janitoo_nosetests.models import JNTTModels,JNTTModelsCommon, jntt_models
from janitoo_nosetests.dbserver import JNTTDBDockerServerCommon, JNTTDBDockerServer, jntt_docker_dbserver

from janitoo.runner import Runner, jnt_parse_args
from janitoo.server import JNTServer
from janitoo.utils import HADD_SEP, HADD

from janitoo.options import JNTOptions
from janitoo_db.base import Base, create_db_engine

import janitoo_db.models as jntmodels

class ModelsCommon(JNTTModelsCommon):
    """Test the models
    """

    def collect_models(self):
        res = {'janitoo' : 'janitoo_db.models'}
        for entrypoint in pkg_resources.iter_entry_points(group='janitoo.models'):
            res[entrypoint.name] = entrypoint.module_name
        return res

    def test_101_user(self):
        self.create_all()
        group = jntmodels.Group(name="test_group")
        user = jntmodels.User(username="test_user", email="test@gmail.com", _password="test", primary_group=group)
        self.dbsession.merge(group, user)
        self.dbsession.commit()

    def test_151_layouts(self):
        self.create_all()
        category = jntmodels.LayoutsCategories(key="key_cat", name="test_cat", description="test_description")
        layout = jntmodels.Layouts(key="key_layout", name="test_layout", description="test_description", layoutcategory=category)
        self.dbsession.merge(category, layout)
        self.dbsession.commit()

    def test_201_lease(self):
        self.create_all()
        now = datetime.datetime.now()
        lease = jntmodels.Lease(add_ctrl="0001", add_node='0001', name="name", location="location", state='BOOT', last_seen=now)
        self.dbsession.merge(lease)
        self.dbsession.commit()

class TestModels(JNTTModels, ModelsCommon):
    """Test the models
    """
    models_conf = "tests/data/janitoo_db.conf"

JNTTBase.skipCITest()
jntt_models(__name__, ModelsCommon, prefix='Db', dbs=[('Postgresql',{'dbconf':'postgresql://janitoo:janitoo@localhost/janitoo_tests'})])
