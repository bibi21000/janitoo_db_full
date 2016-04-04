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
from janitoo_nosetests.models import JNTTModels

from janitoo.options import JNTOptions
from janitoo_db.base import Base, create_db_engine

import janitoo_db.models as jntmodels

class CommonModels(object):
    """Test the models
    """
    janitoo_src = "/opt/janitoo/src"
    def collect_models(self):
        res = {'janitoo' : 'janitoo_db.models'}
        for entrypoint in pkg_resources.iter_entry_points(group='janitoo.models'):
            res[entrypoint.name] = entrypoint.module_name
        return res

    def test_001_user(self):
        self.wipTest()
        group = jntmodels.Group(name="test_group")
        user = jntmodels.User(username="test_user", email="test@gmail.com", _password="test", primary_group=group)
        self.dbsession.merge(group, user)
        self.dbsession.commit()

    def test_051_layouts(self):
        self.wipTest()
        category = jntmodels.LayoutsCategories(key="key_cat", name="test_cat", description="test_description")
        layout = jntmodels.Layouts(key="key_layout", name="test_layout", description="test_description", layoutcategory=category)
        self.dbsession.merge(category, layout)
        self.dbsession.commit()

    def test_101_lease(self):
        self.wipTest()
        now = datetime.datetime.now()
        lease = jntmodels.Lease(add_ctrl="0001", add_node='0001', name="name", location="location", state='BOOT', last_seen=now)
        self.dbsession.merge(lease)
        self.dbsession.commit()

    def test_901_all(self):
        self.wipTest()
        models = self.collect_models()
        import sys
        from os.path import dirname, basename, isfile
        import glob
        modules = []
        for model in models:
            test_dir = os.path.join(self.janitoo_src, model, 'tests')
            print test_dir
            sys.path.append(test_dir) # this is where your python file exists
            modules = [ basename(f)[:-3] for f in glob.glob(test_dir+"/*.py") if isfile(f) and not basename(f).startswith('_')]
            print "Load tests from %s" % modules
            for module in modules:
                #~ __import__(module, locals(), globals())

                __import__(module, locals(), globals())

        eee

class TestModelsSQLite(JNTTModels, CommonModels):
    """Test the models
    """
    models_conf = "tests/data/janitoo_db.conf"

#~ class TestModelsMySQL(JNTTModels, CommonModels):
    #~ """Test the models
    #~ """
    #~ models_conf = "tests/data/janitoo_db_mysql.conf"
#~
#~ class TestModelsPostgresql(JNTTModels, CommonModels):
    #~ """Test the models
    #~ """
    #~ models_conf = "tests/data/janitoo_db_postgres.conf"

