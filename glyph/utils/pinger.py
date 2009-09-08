# This file is a mess :(

import xmlrpclib
import urllib2
from threading import Thread
from django.contrib.sitemaps import ping_google
from django.contrib.sites.models import Site
from django.conf import settings
from tagging.models import Tag

PING_SERVICES = [
    'http://rpc.technorati.com/rpc/ping',
    'http://blogsearch.google.com/ping/RPC2',
    'http://rpc.weblogs.com/RPC2',
    'http://rpc.pingomatic.com',
]

YAHOO = "http://search.yahooapis.com/SiteExplorerService/V1/ping?sitemap=%s"
BING = "http://www.bing.com/webmaster/ping.aspx?siteMap=%s"

def ping_engine(service, url):
    urllib2.urlopen(str(service % url))

class PingThread(Thread):
    
    def __init__(self, obj, feed_url=None):
        self.obj = obj
        self.feed_url = feed_url
        Thread.__init__(self)
        
    def run(self):
        send_pings_for_object(self.obj, self.feed_url)

def send_pings(obj, feed_url):
    t = PingThread(obj, feed_url=feed_url)
    t.run()

def send_pings_for_object(obj, feed_url=None):
    
    if settings.DEBUG:
        print '[DEBUG]: Sending pings for %s' % obj
        return False
    
    result = {}
    
    site = Site.objects.get_current()
    site_url = "http://%s/" % site.domain
    obj_url = "http://%s%s" % (site.domain, obj.get_absolute_url())
    if feed_url is not None:
        feed_url = "http://%s%s" % (site.domain, feed_url)

    ping_success = 0
    ping_fails = 0
    
    # See http://www.weblogs.com/api.html for description of parameters
    args = [
        site.name,
        site_url,
        obj_url,
    ]
    
    if feed_url is not None:
        args.append(feed_url)
        
    if obj.tags:
        tags = Tag.objects.get_for_object(obj)
        tag_list = "|".join([t.name for t in tags])
        args.append(tag_list)
    
    for url in PING_SERVICES:
        try:
            s = xmlrpclib.Server(url)
            try:
                reply = s.weblogUpdates.extendedPing(*args)
            except Exception, e:
                reply =  s.weblogUpdates.ping(*args)
            if reply.get('flerror', False):
                ping_fails += 1
            else:
                ping_success += 1
        except Exception, e:
            reply = 'Pinging %s failed (%s)' % (url, e.message)
            ping_fails += 1
        print reply
        
    result.update({'blogs': 'Blog pings: %s succeeded, %s failed.' % (ping_success, ping_fails)})
    
    try:
        ping_google()
        ping_engine(YAHOO, obj_url)
        ping_engine(YAHOO, site_url)
        ping_engine(BING, obj_url)
        ping_engine(BING, site_url)
    except Exception, e:
        pass
    
    return result
