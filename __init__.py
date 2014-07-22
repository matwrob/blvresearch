# def libs():
#     import os
#     import sys
#     import platform
#     DIR = os.path.dirname(os.path.abspath(__file__))
#     if platform.system() == 'Windows':
#         if platform.architecture()[0] == '64bit':
#             DIR = os.path.join(DIR, 'libs', 'win64')
#         else:
#             DIR = os.path.join(DIR, 'libs', 'win32')
#         if DIR not in sys.path:
#             sys.path.append(DIR)

# libs()
# import logging
# LOG = logging.getLogger('concat')

# from blvprices.universe import Universe, EXCHANGES
