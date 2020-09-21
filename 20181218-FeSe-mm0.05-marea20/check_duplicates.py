#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 17:22:32 2019

@author: Pedram Tavadze
"""

import json
import os
import numpy as np

ls = os.listdir('results')

ls = np.array([re.findall('([0-9]*-[0-9]*_[a-zA-z0-9]*)_',x)[0] for x in ls])






