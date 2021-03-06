#!/usr/bin/env python
#
# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Fraunhofer FKIE/US, Alexander Tiderko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Fraunhofer nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__author__ = "Alexander Tiderko (Alexander.Tiderko@fkie.fraunhofer.de)"
__copyright__ = "Copyright (c) 2012 Alexander Tiderko, Fraunhofer FKIE"
__license__ = "BSD"
__version__ = "0.1"
__date__ = "2012-02-01"

import sys

import roslib; roslib.load_manifest('master_discovery_fkie')
import rospy

from master_monitor import MasterMonitor

MCAST_GROUP = "226.0.0.0" # ipv6 multicast group ff02::1
MCAST_PORT = 11511

def getDefaultRPCPort(zeroconf=False):
  try:
    masteruri = MasterMonitor._masteruri_from_ros()
    rospy.loginfo("ROS Master URI: %s", masteruri)
    from urlparse import urlparse
    return urlparse(masteruri).port+(600 if zeroconf else 300) 
  except:
    import traceback
    print traceback.format_exc()
    return 11911 if zeroconf else 11611

def setTerminalName(name):
  '''
  Change the terminal name.
  @param name: New name of the terminal
  @type name:  str
  '''
  sys.stdout.write("".join(["\x1b]2;",name,"\x07"]))

def setProcessName(name):
  '''
  Change the process name.
  @param name: New process name
  @type name:  str
  '''
  try:
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(name)+1)
    buff.value = name
    libc.prctl(15, byref(buff), 0, 0, 0)
  except:
    pass


def main():
  '''
  Creates and runs the ROS node using multicast messages for discovering
  '''
  import master_discovery
  rospy.init_node("master_discovery", log_level=rospy.DEBUG)
  setTerminalName(rospy.get_name())
  setProcessName(rospy.get_name())
  mcast_group = rospy.get_param('~mcast_group', MCAST_GROUP)
  mcast_port = rospy.get_param('~mcast_port', MCAST_PORT)
  rpc_port = rospy.get_param('~rpc_port', getDefaultRPCPort())
  discoverer = master_discovery.Discoverer(mcast_port, mcast_group, rpc_port)
  discoverer.start()
  rospy.spin()

def main_zeroconf():
  '''
  Creates and runs the ROS node using zeroconf/avahi for discovering
  '''
  import zeroconf
  rospy.init_node("zeroconf", log_level=rospy.DEBUG)
  setTerminalName(rospy.get_name())
  setProcessName(rospy.get_name())
  rpc_port = rospy.get_param('~rpc_port', getDefaultRPCPort(True))
  discoverer = zeroconf.Discoverer(rpc_port)
  discoverer.start()
  rospy.spin()
