# -*- coding: UTF-8 -*-
import sys
import platform
LibVersion = 'Lib25'
if platform.system() == 'Windows':
    path_SvF = "C:/_SvF/"
else :
    path_SvF = "/home/sokol/C/_SvF/"
sys.path.append( path_SvF + LibVersion )
sys.path.append( path_SvF + "Pyomo_Everest/pe" )
   
import COMMON as co
co.path_SvF = path_SvF
co.tmpFileDir = co.path_SvF + 'TMP/'



#from MakeModel import *
from ReadMng import *

#from numpy import *
#from Lego import *
#from GIS import *

Task = ReadMng ( )
