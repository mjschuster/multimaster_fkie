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

import time

import roslib; roslib.load_manifest('master_discovery_fkie')
import rospy

class NodeInfo(object):
  '''
  The NodeInfo class stores informations about a ROS node.
  '''
  def __init__(self, name, masteruri):
    '''
    Creates a new NodeInfo for a node with given name.
    @param name: the name of the node
    @type name: C{str} 
    @param masteruri: the URI of the ROS master, where the node is registered. 
    This masteruri will be used to determine, whether the ROS master and the 
    node are running on the same machine.
    @type masteruri: C{str}
    '''
    self.__name = name
    self.__masteruri = masteruri
    self.__org_masteruri = masteruri
    self.__uri = None
    self.pid = None
    '''@ivar: the process id of the node. Invalid id has a C{None} value'''
    self.__local = False
    self._publishedTopics = []
    self._subscribedTopics = []
    self._services = []

  @property
  def name(self):
    '''
    Returns the name of the node.
    @rtype: C{str}
    '''
    return self.__name

  @property
  def uri(self):
    '''
    Returns the URI of the RPC API of the node.
    @rtype: C{str}
    '''
    return self.__uri

  @uri.setter
  def uri(self, uri):
    '''
    Sets the URI of the RPC API of the node.
    '''
    self.__uri = uri
    self.__local = NodeInfo.local_(self.__masteruri, self.__org_masteruri, self.__uri)

  @property
  def masteruri(self):
    '''
    Returns the URI of the ROS master where the node is registered.
    @rtype: C{str}
    '''
    return self.__org_masteruri

  @masteruri.setter
  def masteruri(self, uri):
    '''
    Sets the ROS master URI.
    '''
    self.__org_masteruri = uri
    self.__local = NodeInfo.local_(self.__masteruri, self.__org_masteruri, self.__uri)

  @property
  def isLocal(self):
    '''
    Returns C{True} if the node and the ROS master are running on the same machine.
    @rtype: C{boolean}
    '''
    return self.__local

  @property
  def publishedTopics(self):
    '''
    Returns the list of all published topics by this node.
    @rtype: C{[str, ...]}
    '''
    return self._publishedTopics
  
  @publishedTopics.setter
  def publishedTopics(self, name):
    '''
    Append a new published topic to this node.
    @param name: the name of the topic
    @type name: C{str} 
    '''
    try:
      if isinstance(name, list):
        del self._publishedTopics
        self._publishedTopics = name
      else:
        self._publishedTopics.index(name)
    except ValueError:
      self._publishedTopics.append(name)

#  @publishedTopics.deleter
#  def publishedTopics(self):
#    del self._publishedTopics

  @property
  def subscribedTopics(self):
    '''
    Returns the list of all subscribed topics by this node.
    @rtype: C{[str, ...]}
    '''
    return self._subscribedTopics
  
  @subscribedTopics.setter
  def subscribedTopics(self, name):
    '''
    Append a new subscribed topic to this node.
    @param name: the name of the topic
    @type name: C{str} 
    '''
    try:
      if isinstance(name, list):
        del self._subscribedTopics
        self._subscribedTopics = name
      else:
        self._subscribedTopics.index(name)
    except ValueError:
      self._subscribedTopics.append(name)

#  @subscribedTopics.deleter
#  def subscribedTopics(self):
#    del self._subscribedTopics

  @property
  def services(self):
    '''
    Returns the list of all services provided by this node.
    @rtype: C{[str, ...]}
    '''
    return self._services
  
  @services.setter
  def services(self, name):
    '''
    Append a new service to this node.
    @param name: the name of the topic
    @type name: C{str} 
    '''
    try:
      if isinstance(name, list):
        del self._services
        self._services = name
      else:
        self._services.index(name)
    except ValueError:
      self._services.append(name)

#  @services.deleter
#  def services(self):
#    del self._services
  
  def copy(self):
    '''
    Creates a copy this object and returns it.
    @rtype: L{NodeInfo} 
    '''
    result = NodeInfo(self.name, self.masteruri)
    result.uri = ''.join([self.uri]) if not self.uri is None else None
    result.pid = self.pid
    result._publishedTopics = list(self._publishedTopics)
    result._subscribedTopics = list(self._subscribedTopics)
    result._services = list(self._services)
    return result

  @staticmethod
  def local_(masteruri, org_masteruri, uri):
    result = False
    try:
      from urlparse import urlparse
      om = urlparse(masteruri)
      on = urlparse(uri)
      try:
        result = (om.hostname == on.hostname) and (masteruri == org_masteruri)
      except:
        pass
    except:
      pass
    return result


class TopicInfo(object):
  '''
  The TopicInfo class stores informations about a ROS topic.
  '''
  def __init__(self, name):
    '''
    Creates a new TopicInfo for a topic with given name.
    @param name: the name of the topic
    @type name: C{str} 
    '''
    self.__name = name
    self.type = None
    '''@ivar: the type of the topic. (Default: None)'''
    self._publisherNodes = []
    self._subscriberNodes = []

  @property
  def name(self):
    '''
    Returns the name of the topic.
    @rtype: C{str}
    '''
    return self.__name

  @property
  def publisherNodes(self):
    '''
    Returns the list with node names witch are publishing to this topic.
    @rtype: C{[str,...]}
    '''
    return list(self._publisherNodes)
  
  @publisherNodes.setter
  def publisherNodes(self, name):
    '''
    Append a new publishing node to this topic.
    '''
    try:
      if isinstance(name, list):
        del self._publisherNodes
        self._publisherNodes = name
      else:
        self._publisherNodes.index(name)
    except ValueError:
      self._publisherNodes.append(name)

#  @publisherNodes.deleter
#  def publisherNodes(self):
#    del self._publisherNodes

  @property
  def subscriberNodes(self):
    '''
    Returns the list with node names witch are subscribed to this topic.
    @rtype: C{[str,...]}
    '''
    return list(self._subscriberNodes)
  
  @subscriberNodes.setter
  def subscriberNodes(self, name):
    '''
    Append a new subscribing node to this topic.
    '''
    try:
      if isinstance(name, list):
        del self._subscriberNodes
        self._subscriberNodes = name
      else:
        self._subscriberNodes.index(name)
    except ValueError:
      self._subscriberNodes.append(name)

#  @subscriberNodes.deleter
#  def subscriberNodes(self):
#    del self._subscriberNodes

  def copy(self):
    '''
    Creates a copy this object and returns it.
    @rtype: L{TopicInfo} 
    '''
    result = TopicInfo(self.name)
    result.type = self.type
    result._publisherNodes = list(self._publisherNodes)
    result._subscriberNodes = list(self._subscriberNodes)
    return result


class ServiceInfo(object):
  '''
  The ServiceInfo class stores informations about a ROS service.
  '''
  def __init__(self, name, masteruri):
    '''
    Creates a new instance of the ServiceInfo. 
    @param name: the name of the service
    @type name: C{str}
    @param masteruri: the URI of the ROS master, where the service is registered. 
    This masteruri will be used to determine, whether the ROS master and the 
    service are running on the same machine.
    @type masteruri: C{str}
    '''
    self.__name = name
    self.__masteruri = masteruri
    self.__org_masteruri = masteruri
    self.__uri = None
    self.__local = False
    self.type = None
    '''@ivar: the type of the service. (Default: None)'''
    self.__service_class = None
    self.args = None
    self.__serviceProvider = []

  @property
  def name(self):
    '''
    Returns the name of the service.
    @rtype: C{str}
    '''
    return self.__name

  @property
  def uri(self):
    '''
    Returns the URI of the RPC API of the service
    @rtype: C{str}
    '''
    return self.__uri

  @uri.setter
  def uri(self, uri):
    '''
    Sets the uri of the service RPC interface and determine whether this service
    and the ROS master are running on the same machine.
    @param uri: The URI of the service RPC interface
    @type uri: C{str}
    '''
    self.__uri = uri
    self.__local = NodeInfo.local_(self.__masteruri, self.__org_masteruri, self.__uri)

  @property
  def masteruri(self):
    '''
    Returns the URI of the ROS master of the service
    @rtype: C{str}
    '''
    return self.__org_masteruri
  
  @masteruri.setter
  def masteruri(self, uri):
    '''
    Sets the uri of the origin ROS master and determine whether this service
    and the ROS master are running on the same machine.
    @param uri: The URI of the ROS master
    @type uri: C{str}
    '''
    self.__org_masteruri = uri
    self.__local = NodeInfo.local_(self.__masteruri, self.__org_masteruri, self.__uri)

  @property
  def isLocal(self):
    '''
    Returns C{True}, if this service and the master are on the same machine. This 
    will be determine on setting the uri-parameter.
    @rtype: C{boolean}
    '''
    return self.__local

  @property
  def serviceProvider(self):
    '''
    Return the list of the node names, which provide this service.
    @rtype: C{[str, ...]}
    '''
    return self.__serviceProvider
  
  @serviceProvider.setter
  def serviceProvider(self, name):
    '''
    Adds a new service provider, if no one with given name exists. 
    @param name: name of the new service provider
    @type name: C{str}
    '''
    try:
      self.__serviceProvider.index(name)
    except ValueError:
      self.__serviceProvider.append(name)

  @serviceProvider.deleter
  def serviceProvider(self):
    del self.__serviceProvider


  def get_service_class(self, allow_get_type=False):
    '''
    Get the service class using the type of the service. NOTE: this
    method is from 'rosservice' and changed to avoid a probe call to the service.
    @param allow_get_type: allow to connect to service and get the type if the 
    type is not valid (in case of other host e.g.)
    @type allow_get_type: C{boolean}
    @return: service class
    @rtype: ServiceDefinition: service class
    @raise ROSServiceException: if service class cannot be retrieved
    '''
    if not self.__service_class is None:
      return self.__service_class

    type = self.type
    # request the type if it is empty and allowed
    if not type and allow_get_type and self.uri:
      dest_addr = dest_port = None
      try:
        dest_addr, dest_port = rospy.parse_rosrpc_uri(self.uri)
      except:
        pass
      else:
        import socket
        import cStringIO
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
          # connect to service and probe it to get the headers
          s.settimeout(0.5)
          s.connect((dest_addr, dest_port))
          header = { 'probe':'1', 'md5sum':'*',
                    'callerid':rospy.get_name(), 'service':self.name}
          roslib.network.write_ros_handshake_header(s, header)
          type = roslib.network.read_ros_handshake_header(s, cStringIO.StringIO(), 2048)
          type = type['type']
        except socket.error:
          pass
        except:
          pass
        finally:
          if s is not None:
            s.close()

    import rosservice
    if not type:
      raise rosservice.ROSServiceException("Not valid type of service [%s]."%str(type))

    # get the Service class so we can populate the request
    service_class = roslib.message.get_service_class(type)

    # #1083: roscpp services are currently returning the wrong type
    if service_class and self.type.endswith('Request') and \
            not hasattr(service_class, "_request_class"):
        type = type[:-7]
        service_class = roslib.message.get_service_class(type)
        
    if service_class is None:
        pkg = roslib.names.resource_name_package(self.type)
        raise rosservice.ROSServiceException("Unable to load type [%s].\n"%self.type+
                                             "Have you typed 'make' in [%s]?"%pkg)
    self.__service_class = service_class
    return service_class


class MasterInfo(object):
  '''
  The MasterInfo class stores informations about a ROS master.
  Not thread safe!
  '''
  def __init__(self, masteruri, mastername = None):
    '''
    Creates a new instance of the MasterInfo. The mastername will be extracted 
    from the masterui, if no name is given.
    @param masteruri: The URI of the corresponding master
    @type masteruri: str
    @param mastername: The name of the ROS master. If no one is given, it will be 
    extracted from the masteruri.
    @type mastername: str or None (Default: None)
    '''
    self.__masteruri = masteruri
    self.__mastername = mastername
    if mastername is None:
      from urlparse import urlparse
      o = urlparse(self.__masteruri)
      self.__mastername = o.hostname
    self.__nodelist = {}
    self.__topiclist = {}
    self.__servicelist = {}
    self.__timestamp = 0
    self.check_ts = 0
    '''@ivar: the last time, when the state of the ROS master retrieved'''

  @staticmethod
  def from_list(l):
    '''
    Creates a new instance of the MasterInfo from given list.
    @see: L{listedState()}
    @param l: the list returned by listedState()
    @type l: list
    @return: the new instance of the MasterInfo filled from list.
    @rtype: MasterInfo
    '''
    if l is None:
      return None
    result = MasterInfo(l[1], l[2])
    result.timestamp = time.time()
    publishers = l[3]
    subscribers = l[4]
    services = l[5]
    topicTypes = l[6]
    nodes = l[7]
    serviceProvider = l[8]
    # set the publishers
    for pub, nodelist in publishers:
      result.topics = pub
      for n in nodelist:
        result.nodes = n
        result.getNode(n).publishedTopics = pub
        result.getTopic(pub).publisherNodes = n
    # set the subscribers
    for sub, nodelist in subscribers:
      result.topics = sub
      for n in nodelist:
        result.nodes = n
        result.getNode(n).subscribedTopics = sub
        result.getTopic(sub).subscriberNodes = n
    # set the services
    for s, provider in services:
      result.services = s
      for n in provider:
        result.nodes = n
        result.getNode(n).services = s
        result.getService(s).serviceProvider = n
    # set the topic types
    for topic, type in topicTypes:
      result.topics = topic
      result.getTopic(topic).type = type
    # set the node informations
    for nodename, uri, masteruri, pid, local in nodes:
      result.nodes = nodename
      result.getNode(nodename).uri = uri
      result.getNode(nodename).masteruri = masteruri
      result.getNode(nodename).pid = pid
    # set the service informations
    for servicename, uri, masteruri, type, local in serviceProvider:
      result.services = servicename
      result.getService(servicename).uri = uri
      result.getService(servicename).masteruri = masteruri
      result.getService(servicename).type = type
    return result

  @property
  def mastername(self):
    '''
    Returns the name of the ROS master. In most cases the ROS master name is the
    name of the host, where the ROS master running. Although it can differ.
    @rtype: C{str}
    '''
    return self.__mastername

  @property
  def masteruri(self):
    '''
    Returns the URI of the ROS master.
    @rtype: C{str}
    '''
    return self.__masteruri

  @property
  def timestamp(self):
    '''
    The timestamp when this MasterInfo was first time filled with the 
    information. See L{self.check_ts} to get the time, when the information was
    compared with the data of ROS Master.
    @rtype: C{float}
    '''
    return self.__timestamp

  @timestamp.setter
  def timestamp(self, ts):
    '''
    Sets the timestamp of this instance
    @param ts: the new timestamp
    @type ts: C{float}
    '''
    self.__timestamp = ts
    self.check_ts = ts

  @property
  def nodes(self):
    '''
    Returns the dictionary with node names and corresponding instances of L{NodeInfo}.
    @rtype: C{dict(str:L{NodeInfo}, ...)}
    '''
    return self.__nodelist

  @nodes.setter
  def nodes(self, name):
    '''
    Adds a new L{NodeInfo} with given name. 
    @note: If the NodeInfo already exists, do nothing.
    @param name: the name of new L{NodeInfo}
    @type name: C{str}
    '''
    if (name is None) or not name:
      return None
    if not (name in self.__nodelist):
      self.__nodelist[name] = NodeInfo(name, self.__masteruri)

  @property
  def node_names(self):
    '''
    Returns the list with node names
    @rtype: C{[str, ...]}
    '''
#    @return: the list with node names
    return self.__nodelist.keys()

  @property
  def node_uris(self):
    '''
    Returns the list with node URI's.
    @rtype: C{[str, ...]}
    '''
    uris = []
    for node in self.__nodelist.itervalues():
      uris.append(node.uri)
    return uris

  @property
  def topics(self):
    '''
    Returns the dictionary with topic names and corresponding L{TopicInfo} instances.
    @rtype: C{dict(str:L{TopicInfo}, ...)}
    '''
    return self.__topiclist

  @topics.setter
  def topics(self, name):
    '''
    Adds a new TopicInfo with given name. If the L{TopicInfo} already exists, do
    nothing.
    @param name: the name of new L{TopicInfo}
    @type name: C{str}
    '''
    if (name is None) or not name:
      return None
    if not (name in self.__topiclist):
      self.__topiclist[name] = TopicInfo(name)

  @property
  def topic_names(self):
    '''
    Returns the list with topic names.
    @rtype: C{[str, ...]}
    '''
    return self.__topiclist.keys()

  @property
  def services(self):
    '''
    Returns the dictionary with service names and corresponding L{ServiceInfo} instances.
    @rtype: C{dict(str:L{ServiceInfo}, ...)}
    '''
    return self.__servicelist

  @services.setter
  def services(self, name):
    '''
    Adds a new L{ServiceInfo} with given name. If the L{ServiceInfo} already exists, do
    nothing.
    @param name: the name of new L{ServiceInfo}
    @type name: C{str}
    '''
    if (name is None) or not name:
      return None
    if not (name in self.__servicelist):
      self.__servicelist[name] = ServiceInfo(name, self.__masteruri)

  @property
  def service_names(self):
    '''
    Returns the list with service names.
    @rtype: C{[str, ...]}
    '''
    return self.__servicelist.keys()

  @property
  def service_uris(self):
    '''
    Returns the list with service URI's.
    @rtype: C{[str, ...]}
    '''
    uris = []
    for service in self.__servicelist.itervalues():
      uris.append(service.uri)
    return uris

  def getNode(self, name):
    '''
    @param name: the name of the node
    @type name: str
    @return: the instance of the L{NodeInfo} with given name
    @rtype: L{NodeInfo} or C{None}
    '''
    if (name is None) or not name:
      return None
    return self.__nodelist.get(name, None)

  def getNodeEndsWith(self, suffix):
    '''
    Returns the node, which name ends with given suffix
    @param suffix: the end of the name
    @type suffix: C{str}
    @return: the instance of the L{NodeInfo} with with given suffix
    @rtype: L{NodeInfo} or C{None}
    '''
    if (suffix is None) or not suffix:
      return None
    for name, node in self.__nodelist.items():
      if name.endswith(suffix):
        return node
    return None

  def getTopic(self, name):
    '''
    @param name: the name of the topic
    @type name: C{str}
    @return: the instance of the L{TopicInfo} with given name
    @rtype: L{NodeInfo} or C{None}
    '''
    if (name is None) or not name:
      return None
    return self.__topiclist.get(name, None)

  def getService(self, name):
    '''
    @param name: the name of the service
    @type name: C{str}
    @return: the instance of the L{ServiceInfo} with given name
    @rtype: L{ServiceInfo} or C{None}
    '''
    if (name is None) or not name:
      return None
    return self.__servicelist.get(name, None)
  
  def __eq__(self, other):
    '''
    Compares the master state with other master state. The timestamp will not be 
    compared.
    @param other: the another L{MasterInfo} instance.
    @type other: L{MasterInfo}
    @return: True, if the states are equal.
    @rtype: C{boolean}
    '''
    if (other is None):
      return False
    if (self.masteruri != other.masteruri):
      return False
    if (set(self.node_uris) ^ set(other.node_uris)):
      return False
    if (set(self.node_names) ^ set(other.node_names)):
      return False
    if (set(self.topic_names) ^ set(other.topic_names)):
      return False
    if (set(self.service_names) ^ set(other.service_names)):
      return False
    if (set(self.service_uris) ^ set(other.service_uris)):
      return False
    # test for changes of each node parameter
    for name in self.node_names:
      n1 = self.getNode(name)
      n2 = other.getNode(name)
      if not n1 is None and not n2 is None:
        if n1.pid != n2.pid:
          return False
        if n1.uri != n2.uri:
          return False
        if set(n1.publishedTopics) ^ set(n2.publishedTopics):
          return False
        if set(n1.subscribedTopics) ^ set(n2.subscribedTopics):
          return False
        if set(n1.services) ^ set(n2.services):
          return False
    return True
  
  def __ne__(self, other):
    return not self.__eq__(other)
  
  def listedState(self):
    '''
    Returns a extended roscore state. 
    @return: complete roscore state as
             
             C{(stamp, masteruri, name, publishers, subscribers, services, topicTypes, nodes, serviceProvider)}
             
               - C{publishers} is of the form
                 
                 C{[ [topic1, [topic1Publisher1...topic1PublisherN]] ... ]}
               
               - C{subscribers} is of the form
                 
                 C{[ [topic1, [topic1Subscriber1...topic1SubscriberN]] ... ]}
               
               - C{services} is of the form
                 
                 C{[ [service1, [service1Provider1...service1ProviderN]] ... ]}
               
               - C{topicTypes} is a list of 
                 
                 C{[ [topicName1, topicType1], ... ]}
               
               - C{nodes} is a list of (the pid of remote Nodes will not be resolved)
                 
                 C{[nodename, XML-RPC URI, origin ROS_MASTER_URI, pid, E{lb} local, remote E{rb}]}
               
               - C{serviceProvider} is a list of (the type, serviceClass and args of remote Services will not be resolved)
                 
                 C{[service, XML-RPC URI, origin ROS_MASTER_URI, type, E{lb} local, remote E{rb}]}
               
    @rtype: C{(float, 
               str,
               str,
               [ [str,[str] ] ], 
               [ [str,[str] ] ], 
               [ [str,[str] ] ], 
               [ [str,str] ], 
               [ [str,str,str,int,str] ], 
               [ [str,str,str,str,str] ])}
    '''
    stamp = str(self.timestamp)
    publishers = []
    subscribers = []
    services = []
    topicTypes = []
    nodes = []
    serviceProvider = []
    for name, topic in self.topics.items():
      pn = topic.publisherNodes
      if pn:
        publishers.append((name, pn))
      sn = topic.subscriberNodes
      if sn:
        subscribers.append((name, sn))
      topicTypes.append((name, topic.type))
    for name, service in self.services.items():
      services.append((name, service.serviceProvider))
      serviceProvider.append((name, service.uri, str(service.masteruri), service.type if not service.type is None else '', 'local' if service.isLocal else 'remote'))
    for name, node in self.nodes.items():
      nodes.append((name, node.uri, str(node.masteruri), node.pid, 'local' if node.isLocal else 'remote'))

    return (stamp, self.masteruri, self.mastername, publishers, subscribers, services, topicTypes, nodes, serviceProvider)
  
#  def __str__(self):
#    return str(self.listedState())
