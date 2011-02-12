import re, string
from lxml import html

NAME            = L('Title')

ART   = 'art-default.jpg'
ICON  = 'icon-default.png'

CTV_ART       = 'ctv-art.jpg'
CTV_ICON      = 'ctv-icon.png'
CTVNEWS_ART	  = ''
CTVNEWS_ICON  = ''
TSN_ART		  = ''
TSN_ICON	  = ''
DISCOVERY_ART = 'discovery-art.jpg'
DISCOVERY_ICON= 'discovery-icon.png'
COMEDY_ART	  = ''
COMEDY_ICON	  = ''
BRAVO_ART	  = ''
BRAVO_ICON	  = ''
BRAVOFACT_ART = ''
BRAVOFACT_ICON= ''
SPACE_ART	  = ''
SPACE_ICON	  = ''
MUCH_ART	  = ''
MUCH_ICON	  = ''
FASHION_ART	  = ''
FASHION_ICON  = ''

VIDEO_PREFIX    = "/video/ctvglobemedia"

#CTV_URL         = 'http://watch.ctv.ca/'
#CTV_SEARCH      = 'http://watch.ctv.ca/AJAX/SearchResults.aspx?query=%s'
#CTV_CLIP_LOOKUP = 'http://watch.ctv.ca/AJAX/ClipLookup.aspx?episodeid=%s'

#CTVNEWS_URL         = 'http://watch.ctv.ca/news/'
#CTVNEWS_SEARCH      = 'http://watch.ctv.ca/news/AJAX/SearchResults.aspx?query=%s'
#CTVNEWS_CLIP_LOOKUP = 'http://watch.ctv.ca/news/AJAX/ClipLookup.aspx?episodeid=%s'

#TSN_URL         = 'http://watch.tsn.ca/'
#TSN_SEARCH      = 'http://watch.tsn.ca/AJAX/SearchResults.aspx?query=%s'
#TSN_CLIP_LOOKUP = 'http://watch.tsn.ca/AJAX/ClipLookup.aspx?episodeid=%s'

#DISCOVERY_URL         = 'http://watch.discoverychannel.ca/'
#DISCOVERY_SEARCH      = 'http://watch.discoverychannel.ca/AJAX/SearchResults.aspx?query=%s'
#DISCOVERY_CLIP_LOOKUP = 'http://watch.discoverychannel.ca/AJAX/ClipLookup.aspx?episodeid=%s'

#COMEDY_URL         = 'http://watch.thecomedynetwork.ca/'
#COMEDY_SEARCH      = 'http://watch.thecomedynetwork.ca/AJAX/SearchResults.aspx?query=%s'
#COMEDY_CLIP_LOOKUP = 'http://watch.thecomedynetwork.ca/AJAX/ClipLookup.aspx?episodeid=%s'

#SPACE_URL         = 'http://watch.spacecast.com/'
#SAPCE_SEARCH      = 'http://watch.spacecast.com/AJAX/SearchResults.aspx?query=%s'
#SPACE_CLIP_LOOKUP = 'http://watch.spacecast.com/AJAX/ClipLookup.aspx?episodeid=%s'

#BRAVO_URL         = 'http://watch.bravo.ca/'
#BRAVO_SEARCH      = 'http://watch.bravo.ca/AJAX/SearchResults.aspx?query=%s'
#BRAVO_CLIP_LOOKUP = 'http://watch.bravo.ca/AJAX/ClipLookup.aspx?episodeid=%s'

#MUCH_URL         = 'http://watch.muchmusic.com/'
#MUCH_SEARCH      = 'http://watch.muchmusic.com/AJAX/SearchResults.aspx?query=%s'
#MUCH_CLIP_LOOKUP = 'http://watch.muchmusic.com/AJAX/ClipLookup.aspx?episodeid=%s'

#FASHION_URL         = 'http://watch.fashiontelevision.com/'
#FASHION_SEARCH      = 'http://watch.fashiontelevision.com/AJAX/SearchResults.aspx?query=%s'
#FASHION_CLIP_LOOKUP = 'http://watch.fashiontelevision.com/AJAX/ClipLookup.aspx?episodeid=%s'

URL		= 'http://watch.%s/'
LIBRARY_URL     = 'http://watch.%s/library/'
SEARCH_URL	= 'http://watch.%s/AJAX/SearchResults.aspx?query=%s'
CLIP_LOOKUP	= 'http://watch.discoverychannel.ca/AJAX/ClipLookup.aspx?episodeid=%s'

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, NAME, ICON, ART)
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'CTVGlobeMedia'
  MediaContainer.content = 'Items'
  MediaContainer.art = R(ART)
  MediaContainer.thumb = R(ICON)
  HTTP.CacheTime = 1800

####################################################################################################

def MainMenu():
  dir = MediaContainer(ViewGroup='List')
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('CTV'), thumb=R(CTV_ICON), art=R(CTV_ART)), network='ctv.ca'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('CTV News'), thumb=R(CTVNEWS_ICON), art=R(CTVNEWS_ART)), network='ctv.ca/news'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('TSN'), thumb=R(TSN_ICON), art=R(TSN_ART)), network='tsn.ca'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('Discovery Channel'), thumb=R(DISCOVERY_ICON), art=R(DISCOVERY_ART)), network='discoverychannel.ca'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('The Comedy Network'), thumb=R(COMEDY_ICON), art=R(COMEDY_ART)), network='thecomedynetwork.ca'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('Bravo!'), thumb=R(BRAVO_ICON), art=R(BRAVO_ART)), network='bravo.ca'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('Bravo!Fact'), thumb=(BRAVOFACT_ICON), art=(BRAVOFACT_ART)), network='bravofact.com'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('Space'), thumb=R(SPACE_ICON), art=R(SPACE_ART)), network='spacecast.com'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('MuchMusic'), thumb=R(MUCH_ICON), art=R(MUCH_ART)), network='muchmusic.com'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('Fashion Television'), thumb=R(FASHION_ICON), art=R(FASHION_ART)), network='fashiontelevision.com'))
  return dir

####################################################################################################

#def GetURL(network):
#  
#  if network == 'CTV':
#    return CTV_URL
#  elif network == 'CTV News':
#    return CTVNEWS_URL
#  elif network == 'Discovery':
#    return DISCOVERY_URL
#  elif network == 'Comedy':
#    return COMEDY_URL
#  elif network == 'Bravo':
#    return BRAVO_URL
#  elif network == 'Space':
#    return SPACE_URL
#  elif network == 'MuchMusic':
#    return MUCH_URL
#  elif network == 'Fashion':
#    return FASHION_URL
#  else:
#    return 'unknown'

####################################################################################################

#def GetSearchURL(network):
#  
#  if network == 'CTV':
#    return CTV_SEARCH
#  elif network == 'CTV News':
#    return CTVNEWS_SEARCH
#  elif network == 'Discovery':
#    return DISCOVERY_SEARCH
#  elif network == 'Comedy':
#    return COMEDY_SEARCH
#  elif network == 'Bravo':
#    return BRAVO_SEARCH
#  elif network == 'Space':
#    return SPACE_SEARCH
#  elif network == 'MuchMusic':
#    return MUCH_SEARCH
#  elif network == 'Fashion':
#    return FASHION_SEARCH
#  else:
#    return 'unknown'

####################################################################################################

#def GetClipLookup(network):
#  
#  if network == 'CTV':
#    return CTV_CLIP_LOOKUP
#  elif network == 'CTV News':
#    return CTVNEWS_CLIP_LOOKUP
#  elif network == 'Discovery':
#    return DISCOVERY_CLIP_LOOKUP
#  elif network == 'Comedy':
#    return COMEDY_CLIP_LOOKUP
#  elif network == 'Bravo':
#    return BRAVO_CLIP_LOOKUP
#  elif network == 'Space':
#    return SPACE_CLIP_LOOKUP
#  elif network == 'MuchMusic':
#    return MUCH_CLIP_LOOKUP
#  elif network == 'Fashion':
#    return FASHION_CLIP_LOOKUP
#  else:
#    return 'unknown'

####################################################################################################

def VideoMenu(sender, network):
  dir = MediaContainer(ViewGroup='List', title2=sender.itemTitle, art=sender.art)
  dir.Append(Function(DirectoryItem(GetFeatured, title="Featured"), network=network, title2="Featured"))
  dir.Append(Function(DirectoryItem(GetVideoLibrary, title="Video Library"), level=1, url=((URL % network)+'library/'), title2="Video Library"))
  dir.Append(Function(InputDirectoryItem(Search, title=L("Search"), prompt=L("Search for Videos"), thumb=R('search.png'))))
  return dir

####################################################################################################

def GetVideoLibrary(sender, url, level, title2):
  dir = MediaContainer(title2=title2)
  if title2 == 'CTV Documentaries':
    for show in HTML.ElementFromURL(url).xpath('//div[@id="Level%d"]/ul/li' % level):
      title = None
      url = url    
      try: title = show.find('a').get('title')
      except: pass
      try: url = show.find('a').get('href')
      except: pass
      if level == 2:
        #Log('Add a webvideo item')
        try: summary =  item.find('dd[@class="Description"]' ).text 
        except: summary ="No Summary Available" 
        thumb =  show.xpath('//dd[@class="Thumbnail"]/a/img')[0].get('src')
        #Log(thumb)
        dir.Append(WebVideoItem(url, title, date="", summary=summary, thumb=Function(GetThumb, thumb)))    
      else:
        dir.Append(Function(DirectoryItem(GetVideoLibrary, title, thumb=R('icon-default.png')), level=level+1, url=url, title2=title))
  elif title2 == 'CTV Movie':
    for show in HTML.ElementFromURL(url).xpath('//div[@id="Level%d"]/ul/li' % level):
      title = None
      url = url    
      try: title = show.find('a').get('title')
      except: pass
      try: url = show.find('a').get('href')
      except: pass
      if level == 2:
        #Log('Add a webvideo item')
        try: summary =  item.find('dd[@class="Description"]' ).text 
        except: summary ="No Summary Available" 
        thumb =  show.xpath('//dd[@class="Thumbnail"]/a/img')[0].get('src')
        #thumb = thumb.replace('80/60', '512/384')
        #Log(thumb)
        dir.Append(WebVideoItem(url, title, date="", summary=summary, thumb=thumb))    
      else:
        dir.Append(Function(DirectoryItem(GetVideoLibrary, title, thumb=R('icon-default.png')), level=level+1, url=url, title2=title))
  else:
    for show in HTML.ElementFromURL(url).xpath('//div[@id="Level%d"]/ul/li' % level):
      title = None
      url = url    
      try: title = show.find('a').get('title')
      except: pass
      try: url = show.find('a').get('href')
      except: pass
      playable = ''
      try: playable = show.xpath('.//dd[@class="Play"]/a')[0].get('title')
      except: pass
      if playable:
        #Log('Add a webvideo item')
        try: title = show.xpath('.//dl[@class="Item"]/dt/a')[0].text
        except:pass
        #Log(title)
        try: summary =  show.xpath('.//dd[@class="Description"]')[0].text 
        except: summary ="No Summary Available" 
        thumb =  show.xpath('//dd[@class="Thumbnail"]/a/img')[0].get('src')
        #thumb = thumb.replace('80/60', '512/384')
        #Log(thumb)
        dir.Append(WebVideoItem(url, title, date="", summary=summary, thumb=thumb))    
      else:
        dir.Append(Function(DirectoryItem(GetVideoLibrary, title, thumb=R('icon-default.png')), level=level+1, url=url, title2=title))
  return dir

####################################################################################################

def GetFeatured(sender, network, title2):
  dir = MediaContainer(title2=title2)
  for show in HTML.ElementFromURL((URL % network) + 'featured/').xpath('//div[@class="Frame"]/ul/li'):    
    try:
      item = show.xpath('.//dl[@class="Item"]')[0]    
      title = item.find('dt/a').get('title')
      url = item.find('dt/a').get('href')
      #Log('Title: %s  URL: %s' % (title, url))
      try: summary = item.find('dd[@class="Description"]').text
      except: summary = "No Summary Available" 
      thumb =  item.find('dd[@class="Thumbnail"]/a/img').get('src')
      #thumb = thumb.replace('80/60', '512/384')
      #Log(thumb)
      dir.Append(WebVideoItem(url, title, date="", summary=summary, thumb=thumb))    
    except: pass    
  return dir

################################################################################

def GetVideoFromEpisodeId(episodeId, network):
  show = HTTP.Request(CLIP_LOOKUP %(network, episodeId)).content
  #Log(show)
  expression = re.compile("EpisodePermalink:'(.+?)'", re.MULTILINE)
  #Log(expression)
  url = expression.search(show).group(1)
  #Log(url)
  return url

################################################################################

def Search(sender, network, query):
  dir = MediaContainer(viewGroup='Details', title2='Search Results')
  query = query.replace(' ', '+')
  searchResults = HTML.ElementFromURL(SEARCU_URL % (network, query))
  #Log(searchResults)
  for result in searchResults.xpath('//li'):
    #Log(result.xpath('.//dl')[0].get('class'))
    if result.xpath('.//dl')[0].get('class') != "NotPlayable":      
      try:
        try:
          result.find('.//b').drop_tag()
          result.find('.//strong').drop_tag()
        except: pass 
        title = result.xpath('./dl/dd[@class="ResultTitle"]/a')[0].text
        #Log(title)
        try: summary = result.xpath('./dl/dd[@class="ResultDescription"]').text
        except: summary = "No Description Available"
        #Log(summary)
        thumb = result.find('dl/dd[@class="SearchThumbnail"]/a/img').get('src')
        #thumb = thumb.replace('80/60', '512/384')
        #Log(thumb)
        episodeId = result.xpath('./dl/dd[@class="PlayNow"]/a')[0].get('href')
        #Log(episodeId)
        episodeId = episodeId.split('PlayEpisode(')[1].replace(")", "")
        #Log(episodeId)
        url = GetVideoFromEpisodeId(episodeId)
        #Log(url)
        dir.Append(WebVideoItem(url, title, date="", summary=summary, thumb=thumb))            
      except: pass      
  return dir

################################################################################

def GetThumb(url):
    '''A function to return thumbs.'''
    url = url.replace('80/60', '512/384')
    #Log(url)
    try:
        data = HTTP.Request(url, cacheTime=CACHE_1MONTH)
        return DataObject(data, 'image/jpeg')
    except:
        return Redirect(R(ICON))
        
################################################################################



