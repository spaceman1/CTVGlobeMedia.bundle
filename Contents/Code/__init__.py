import re, string
from lxml import html

NAME            = L('Title')

ART   = 'art-default.jpg'
ICON  = 'icon-default.png'

VIDEO_PREFIX    = "/video/ctv"
CTV_URL         = 'http://watch.ctv.ca/'
CTV_SEARCH      = 'http://watch.ctv.ca/AJAX/SearchResults.aspx?query=%s'
CTV_CLIP_LOOKUP = 'http://watch.ctv.ca/AJAX/ClipLookup.aspx?episodeid=%s'

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, NAME, ICON, ART)
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'CTV.ca'
  MediaContainer.content = 'Items'
  MediaContainer.art = R(ART)
  MediaContainer.thumb = R(ICON)
  HTTP.CacheTime = 1800

####################################################################################################

def MainMenu():
  dir = MediaContainer()
  dir.Append(Function(DirectoryItem(GetFeatured, title="Featured"), url= CTV_URL + 'featured/', title2="Featured"))
  dir.Append(Function(DirectoryItem(GetVideoLibrary, title="Video Library"), url= CTV_URL + 'library/', level=1, title2="Video Library"))
  dir.Append(Function(InputDirectoryItem(Search, title=L("Search"), prompt=L("Search for Videos"), thumb=R('search.png'))))
  return dir

####################################################################################################

def GetVideoLibrary(sender, level, url, title2):
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
        Log('Add a webvideo item')
        try: summary =  item.find('dd[@class="Description"]' ).text 
        except: summary ="No Summary Available" 
        thumb =  show.xpath('//dd[@class="Thumbnail"]/a/img')[0].get('src')
        Log(thumb)
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
        Log('Add a webvideo item')
        try: summary =  item.find('dd[@class="Description"]' ).text 
        except: summary ="No Summary Available" 
        thumb =  show.xpath('//dd[@class="Thumbnail"]/a/img')[0].get('src')
        thumb = thumb.replace('80/60', '512/384')
        Log(thumb)
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
      if level == 3:
        Log('Add a webvideo item')
        try: summary =  item.find('dd[@class="Description"]' ).text 
        except: summary ="No Summary Available" 
        thumb =  show.xpath('//dd[@class="Thumbnail"]/a/img')[0].get('src')
        thumb = thumb.replace('80/60', '512/384')
        Log(thumb)
        dir.Append(WebVideoItem(url, title, date="", summary=summary, thumb=thumb))    
      else:
        dir.Append(Function(DirectoryItem(GetVideoLibrary, title, thumb=R('icon-default.png')), level=level+1, url=url, title2=title))
  return dir

####################################################################################################

def GetFeatured(sender, url, title2):
  dir = MediaContainer(title2=title2)
  for show in HTML.ElementFromURL(url).xpath('//div[@class="Frame"]/ul/li'):    
    try:
      item = show.xpath('.//dl[@class="Item"]')[0]    
      title = item.find('dt/a').get('title')
      url = item.find('dt/a').get('href')
      #Log('Title: %s  URL: %s' % (title, url))
      try: summary = item.find('dd[@class="Description"]').text
      except: summary = "No Summary Available" 
      thumb =  item.find('dd[@class="Thumbnail"]/a/img').get('src')
      thumb = thumb.replace('80/60', '512/384')
      Log(thumb)
      dir.Append(WebVideoItem(url, title, date="", summary=summary, thumb=thumb))    
    except: pass    
  return dir

################################################################################

def GetVideoFromEpisodeId( episodeId):
  show = HTTP.Request(CTV_CLIP_LOOKUP % episodeId).content
  #Log(show)
  expression = re.compile("EpisodePermalink:'(.+?)'", re.MULTILINE)
  #Log(expression)
  url = expression.search(show).group(1)
  #Log(url)
  return url

################################################################################

def Search(sender, query):
  dir = MediaContainer(viewGroup='Details', title2='Search Results')
  query = query.replace(' ', '+')
  searchResults = HTML.ElementFromURL(CTV_SEARCH % query)
  #Log(searchResults)
  for result in searchResults.xpath('//li'):
    Log(result.xpath('.//dl')[0].get('class'))
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

def GetThumb(url):
    '''A function to return thumbs.'''
    url = url.replace('80/60', '512/384')
    Log(url)
    try:
        data = HTTP.Request(url, cacheTime=CACHE_1MONTH)
        return DataObject(data, 'image/jpeg')
    except:
        return Redirect(R(ICON))
        
################################################################################
