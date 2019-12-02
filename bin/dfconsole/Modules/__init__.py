#This file allows the import syntax "from Modules import *"
#That way you can throw new modules in the folder and import dynamically.

from os.path import dirname, basename, isfile
import glob

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) if not f.endswith('__init__.py')]