import urllib.request  # 
import json            # json.loads()
import re              # re.search(), re.findall()
import numpy as np     #
# import os              # makedir()

class Crawl(object):
  url = ''

  def __init__(self, url):
    self.url = url

  def req_page(self, url, cache_flag=False):
    if not url:
      url = self.url
    try:
      with urllib.request.urlopen(url) as resp:  # <http.client.HTTPResponse>
        url_data = resp.read().decode('UTF-8')  # <bytes> -> <str>
      try:
        return json.loads(url_data)  # <str> -> <dict>
      except json.decoder.JSONDecodeError:
        return url_data  # <str>
      except:
        print('unknown error')
    except urllib.error.HTTPError:
      print('HTTP Error')  # HTTP Error 404: Not Found (account not exists)
      # HTTP Error 405: Method Not Allowed

  @staticmethod
  def download_pic(url, dir=""):
    regex_pic_name = r"([\w]+.jpg)"
    pic_name = re.search(regex_pic_name, url).group()
    if not dir:
      file_name = pic_name
    else:
      file_name = "{}/{}".format(dir, pic_name)
    urllib.request.urlretrieve(url, file_name)

class Crawl_IG(Crawl):
  HOMEPAGE       = "https://www.instagram.com"
  LOGINPAGE      = "{home}/{account}/login"
  API_POSTFIX    = "?__a=1"  # for profile and post
  PROFILE_FMT    = "{home}/{account}/{api}"
  POST_FMT       = "{home}/p/{shortcode}/{api}"
  HD_PROFILE_FMT = "https://i.instagram.com/api/v1/users/{user_id}/info"
  # USER_MEDIA_FMT = "https://instagram.com/graphql/query/?query_id=17888483320059182&id={user_id}&first={req_post_cnt}&after={end_cursor}"  # req_post_cnt: 12 default, 50 max
  USER_MEDIA_FMT = "{home}/graphql/query/?query_hash={query_hash}&variables={variables}"  # req_post_cnt: 12 default, 50 max
  # 2019-08-10: new way by query_hash, variables {id, first, after}
  PROFILE_CONTAINER_FMT = "{home}/{container}"

  IG_info = {
    'account': '',
    'user_id': 0,
    'query_hash': '',
    'queryId': [] 
  }
  IG_media = {
    'page_cnt': 0, 
    'post_cnt': 0,
    'post_capacity': 0,
    'end_cursor': '', 
    'pages': np.empty(128, dtype='<U128'),  # page token
    'shortcodes': np.empty(1024, dtype='<U16')  # post token
  }
  profile_cache    = {}
  profile_container_cache  = {}
  hd_profile_cache = {}
  user_media_cache = {}

  pic_url = []
  post_url = []
  all_pic_url = np.empty(1024, dtype='<U256')

  REGEX = {
    'account': r"(?<=www.instagram.com\/)([\w\-.]+)",
    'shareData': r"(?<=<script type=\"text/javascript\">window._sharedData = )(.*)(?=;</script>)",
    'container': r"(?<=\"/)([^\"]+ProfilePageContainer.js[^\"]+)(?=\")",
    'query_hash': r"profilePosts.*queryId:\"([^\"]+)",
    'queryId': r"(?<=queryId:\")([^\"]+)(?=\")"
  }

  def __init__(self, url):
    self.get_user_info(url)

  def req_profile_page(self, account):
    """get profile json by api url"""
    profile_url = self.PROFILE_FMT.format( \
      home=self.HOMEPAGE, account=account, api=self.API_POSTFIX)
    try:
      self.profile_cache = self.req_page(profile_url)
    except:
      print("error")

  def req_profile_html(self, account):
    """get profile html by url"""
    profile_url = self.PROFILE_FMT.format( \
      home=self.HOMEPAGE, account=account, api="")
    html_str = self.req_page(profile_url)  # html <str>
    # extract profile from .window._shareData
    self.profile_cache = json.loads(re.search(self.REGEX['shareData'], \
                                              html_str).group())  # <dict>
    # retrieve ProfilePageContainer.js
    container_path = re.search(self.REGEX['container'], html_str).group()
    container_url = self.PROFILE_CONTAINER_FMT.format( \
      home=self.HOMEPAGE, container=container_path)
    self.profile_container_cache = self.req_page(container_url)

  def req_hd_profile_page(self):
    """get hd profile data by api url"""
    hd_profile_url = self.HD_PROFILE_FMT.format( \
      user_id=self.IG_info['user_id'])
    try:
      self.hd_profile_cache = self.req_page(hd_profile_url)
    except:
      print("error")

  def req_user_media_page(self, req_post_cnt=12, end_cursor=''):
    """get user media data by api url"""
    variables = dict(zip(('id', 'first', 'after'), 
                         (self.IG_info['user_id'], req_post_cnt, end_cursor)))
    user_media_url = self.USER_MEDIA_FMT.format( \
      home=self.HOMEPAGE, 
      query_hash=self.IG_info['query_hash'], 
      variables=json.dumps(variables, separators=(',', ':')))  # no spaces
    try:
      self.user_media_cache = self.req_page(user_media_url)
    except:
      print("error")

  def req_post_html(self, shortcode):
    post_url = self.POST_FMT.format( \
      home=self.HOMEPAGE, shortcode=shortcode, api="")
    print(post_url)
    html_str = self.req_page(post_url)  # html <str>
    self.post_cache = json.loads(re.search(self.REGEX['shareData'], \
                                           html_str).group())
    page_dict = self.post_cache['entry_data']['PostPage'][0]
    pic_url = page_dict['graphql']['shortcode_media']['display_resources'][-1]['src']
    print(pic_url)
    return pic_url

  def get_user_info(self, url):
    # try:
      account = re.search(self.REGEX['account'], url).group()
      # self.req_profile_page(account)
      self.req_profile_html(account)
      ### need to interrupt if account not exists
      page_dict = self.profile_cache['entry_data']['ProfilePage'][0]
      self.IG_info['account'] = account
      self.IG_info['user_id'] = page_dict['graphql']['user']['id']
      self.IG_info['query_hash'] = \
        re.search(self.REGEX['query_hash'], \
                  self.profile_container_cache).groups()[0]
      self.IG_info['queryId'] = \
        re.findall(self.REGEX['queryId'], self.profile_container_cache)
      self.IG_media['post_capacity'] = \
        page_dict['graphql']['user']['edge_owner_to_timeline_media']['count']
    # except:
      # print("error")

  def dl_user_hd_profile_pic(self):
    #
    self.req_hd_profile_page()
    hd_profile_url = self.hd_profile_cache \
      ['user']['hd_profile_pic_url_info']['url']
    self.download_pic(hd_profile_url)

  def get_page(self, end_cursor=''):
    post_cnt = self.IG_media['post_cnt']
    post_cap = self.IG_media['post_capacity']
    page_cnt = self.IG_media['page_cnt']
    if post_cnt == post_cap:
      return
    elif end_cursor == '_NEXT':
      end_cursor = self.IG_media['end_cursor']
    # try:
    self.req_user_media_page(end_cursor=end_cursor)
    next_page = self.user_media_cache['data']['user'] \
      ['edge_owner_to_timeline_media']['page_info']['end_cursor']
    self.IG_media['end_cursor'] = next_page
    edges = self.user_media_cache['data']['user'] \
      ['edge_owner_to_timeline_media']['edges']  # list
    if edges:
      self.IG_media['page_cnt'] += 1
    if next_page:
      self.IG_media['pages'][page_cnt+1] = self.IG_media['end_cursor']
    shortcode = [nodes['node']['shortcode'] for nodes in edges]
    self.IG_media['post_cnt'] += len(shortcode)
    prev_idx = post_cnt
    curr_idx = self.IG_media['post_cnt']
    self.IG_media['shortcodes'][prev_idx:curr_idx] = np.array(shortcode)
    print("page: {:3d}, post: {:5d} / {:5d}".format( \
      self.IG_media['page_cnt'], self.IG_media['post_cnt'], \
      self.IG_media['post_capacity']))
    # except:
      # print("error")

  def get_all_page(self):
    # curr_page = ''
    while True:
      # next_page = self.IG_media['end_cursor']
      self.get_page(end_cursor='_NEXT')
      if not self.IG_media['end_cursor']:
        break

  def parse_post(self):
    page_dict = self.post_cache['entry_data']['PostPage'][0]
    pic_url = page_dict['graphql']['shortcode_media']['display_resources'][-1]['src']
    return pic_url
    
  def get_all_pic(self):
    post_cnt = self.IG_media['post_cnt']
    shortcodes = self.IG_media['shortcodes']
    t = tuple(self.req_post_html(shortcodes[post_idx]) for post_idx in range(post_cnt))
    self.all_pic_url[:post_cnt] = np.array(t)
  def dl_pic_url(self):
    pass

if __name__ == '__main__':
  # url = "https://www.instagram.com/nisustim/"  # not exist
  url = "https://www.instagram.com/veronicarehab/"
  # url = "https://www.instagram.com/rubis_03/"
  c = Crawl_IG(url)
  c.get_all_page()
