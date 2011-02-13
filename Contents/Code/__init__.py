import re, string
from lxml import html

NAME            = L('Title')

ART   = 'art-default.jpg'
ICON  = 'icon-default.png'

CTV_ART       = 'art-ctv.jpg'
CTV_ICON      = 'icon-ctv.png'
CTVNEWS_ART   = 'art-ctvnews.jpg'
CTVNEWS_ICON  = 'icon-ctvnews.png'
TSN_ART       = 'art-tsn.jpg'
TSN_ICON      = 'icon-tsn.png'
DISCOVERY_ART = 'art-discovery.jpg'
DISCOVERY_ICON= 'icon-discovery.png'
COMEDY_ART    = 'art-comedy.jpg'
COMEDY_ICON   = 'icon-comedy.png'
BRAVO_ART     = 'art-bravo.jpg'
BRAVO_ICON    = 'icon-bravo.png'
BRAVOFACT_ART = 'art-bravofact.jpg'
BRAVOFACT_ICON= 'icon-bravofact.png'
SPACE_ART     = 'art-space.jpg'
SPACE_ICON    = 'icon-space.png'
MUCH_ART      = 'art-much.jpg'
MUCH_ICON     = 'icon-much.png'
FASHION_ART   = 'art-fashion.jpg'
FASHION_ICON  = 'icon-fashion.png'

VIDEO_PREFIX    = "/video/ctvglobemedia"

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
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('Bravo!Fact'), thumb=R(BRAVOFACT_ICON), art=R(BRAVOFACT_ART)), network='bravofact.com'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('Space'), thumb=R(SPACE_ICON), art=R(SPACE_ART)), network='spacecast.com'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('MuchMusic'), thumb=R(MUCH_ICON), art=R(MUCH_ART)), network='muchmusic.com'))
  dir.Append(Function(DirectoryItem(VideoMenu, title=L('Fashion Television'), thumb=R(FASHION_ICON), art=R(FASHION_ART)), network='fashiontelevision.com'))
  return dir

####################################################################################################

def VideoMenu(sender, network):
  dir = MediaContainer(ViewGroup='List', title2=sender.itemTitle, art=sender.art)
  dir.Append(WebVideoItem(URL % network, title='Just Watch', subtitle='Continuous play', date='',
    summary="Don't care what you watch? Just watch whatever's on!", thumb = sender.thumb))
  dir.Append(Function(DirectoryItem(GetFeatured, title="Featured"), network=network, title2="Featured"))
  dir.Append(Function(DirectoryItem(GetVideoLibrary, title="Video Library"), level=1, url=((URL % network)+'library/'), title2="Video Library"))
  dir.Append(Function(InputDirectoryItem(Search, title=L("Search"), prompt=L("Search for Videos"), thumb=R('search.png'))))
  return dir

####################################################################################################

def GetVideoLibrary(sender, url, level, title2):
  dir = MediaContainer(title2=title2)
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
      try:
        thumb =  show.xpath('.//dd[@class="Thumbnail"]/a/img')[0].get('src')
        thumb = thumb.replace('80/60', '512/384')
      except:
        thumb = sender.thumb
      #Log(thumb)
      dir.Append(WebVideoItem(url, title, date="", summary=summary, thumb=thumb))    
    else:
      dir.Append(Function(DirectoryItem(GetVideoLibrary, title, thumb=sender.thumb), level=level+1, url=url, title2=title))
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
      thumb = thumb.replace('80/60', '512/384')
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
  searchResults = HTML.ElementFromURL(SEARCH_URL % (network, query))
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
        thumb = thumb.replace('80/60', '512/384')
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



