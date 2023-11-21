__all__ = ['flatten_boxscore', 'Page', 'LinescorePage']

# Cell

import requests
from requests.models import Response
from bs4 import BeautifulSoup,Tag
from abc import ABC, abstractproperty
from dataclasses import dataclass
from typing import List, Any
from collections import defaultdict
from hashlib import sha256

# Internal Cell

def make_request_from(
     *
    ,url : str
    ,**kwargs
)->Response:
    return requests.get(url=url, **kwargs)


def make_soup_from(
     *
    ,response : Response
    ,**kwargs
)->BeautifulSoup:
    """ Returns a Beautifulsoup object for the passed URL."""

    return BeautifulSoup(response.content,features='html.parser',**kwargs)

# Internal Cell

def generate_dict_from_table(
    table : Tag
)->defaultdict:
    """Helper function for returning the curling boxscore from a bs4 Tag object."""
    d = defaultdict(list)
    team = None

    # TODO : add error handling for when no table is passed / None

    if table is None:
        raise ValueError('Table tag is NoneType.')

    # loop through tags in table
    for tag in table.find_all('td'):
        if tag.attrs.get('class') == ['linescoreteam']:
            team = tag.a.string
            d[team] = defaultdict(list)
            d[team]['href'] = tag.a['href']
        elif tag.attrs.get('class') == ['linescorehammer']:
            d[team]['hammer'] = not bool(tag.string) # opposite for some reason
        elif tag.attrs.get('class') == ['linescoreend']:
            d[team]['score'].append(tag.string.strip())
        elif tag.attrs.get('class') == ['linescorefinal']:
            d[team]['finalscore'] = tag.b.string.strip()

    return d

# Cell
def flatten_boxscore(
    boxscore : defaultdict
)->List[List[Any]]:
    return [[team_name,*list(stats.values())] for team_name, stats in boxscore.items()]

# Internal Cell

def hash_obj(
     obj : Any
    ,hash_type : str = 'sha256'
    ,encoding : str='utf-8'
)->str:
    """Hashes an object according to the passed hash_type and encoding."""
    hash_type = hash_type.lower()
    encoding = encoding.lower()

    if hash_type == 'sha256':
        hash_func = sha256
    else:
        raise NotImplementedError("Hash function %s not supported."%hash_type)

    return hash_func(str(obj).encode(encoding)).hexdigest().lower()

# Cell


class Page(ABC):

    def __post_init__(self)->None:
        response = make_request_from(url = self.url)
        self.soup = make_soup_from(response=response)
        try:
            self.boxscores = self.generate_boxscores()
        except:
            pass

    @abstractproperty
    def url(self)->str:
        ...
'''
    @abstractproperty
    def event_name(self)->str:
        ...

    @abstractproperty
    def event_date(self)->str:
        ...

    @abstractproperty
    def draw(self)->str:
        ...

    @abstractproperty
    def tables(self)->List[Tag]:
        ...

    @abstractmethod
    def generate_boxscores(self)->List[dict]:
        ...
'''

@dataclass
class LinescorePage(Page):
    cz_event_id : int
    cz_draw_id: int


    @property
    def url(self)->str:
        return 'https://curlingzone.com/event.php?eventid=%s&view=Scores&showdrawid=%s#1'%(self.cz_event_id,self.cz_draw_id)

    @property
    def event_name(self)->str:
        return self.soup.find('h3',attrs={'class':'entry-title-widget'}).string

    @property
    def event_date(self)->str:
        return self.soup.find('div',attrs={'class':'badge-widget'}).string

    @property
    def draw(self)->str:
        return self.soup.find(name='option',attrs={'selected':'selected'}).string

    @property
    def tables(self)->List[Tag]:
        return self.soup.find_all(name = 'table',attrs={'class':'linescorebox'})

    def generate_boxscores(self)->List[defaultdict]:
        try:
            return [generate_dict_from_table(table=table) for table in self.tables]
        except:
            return []

    def get_boxscore_from(self,cz_game_id : int)->defaultdict:
        if cz_game_id <= 0:
            raise ValueError('cz_game_id must be 1 or greater.')

        if cz_game_id > len(self.boxscores):
            raise ValueError('') # TODO

        return self.boxscores[cz_game_id - 1]

@dataclass
class EventPage(Page):
    cz_event_id : int

    @property
    def url(self)->str:
        return 'https://curlingzone.com/event.php?view=Main&eventid=%s#1'%(self.cz_event_id)

    @property
    def event_name(self)->str:
        return self.soup.find('h3',attrs={'class':'entry-title-widget'}).string

    @property
    def event_date(self)->str:
        daterange = self.soup.find('div',attrs={'class':'badge-widget'}).string
        from datetime import datetime
        try:
            startdate = daterange[:daterange.index('-')] + daterange[-4:]
        except:
            startdate = daterange
        try:
            dt = datetime.strptime(startdate, '%b %d %Y').date()
            return dt.strftime('%Y-%m-%d')
        except:
            return "Null"
    
    @property
    def event_type(self)->str:
        pretty = self.soup.prettify()
        if "eventtypeid=1&" in pretty:
            return 'Mixed'
        if ("eventtypeid=81&" in pretty or "eventtypeid=2&" in pretty 
            or "eventtypeid=31&" in pretty or "eventtypeid=32&" in pretty 
            or "eventtypeid=33&" in pretty or "eventtypeid=34&" in pretty
            or "eventtypeid=35&" in pretty or "eventtypeid=37&" in pretty
            or "eventtypeid=23&" in pretty or "eventtypeid=21&" in pretty
            or "eventtypeid=9&"  in pretty or "eventtypeid=501&" in pretty
            or "eventtypeid=41&" in pretty or "eventtypeid=10&" in pretty
            or "eventtypeid=101&" in pretty or "eventtypeid=0&" in pretty
            or "eventtypeid=503&" in pretty or "eventtypeid=38&" in pretty
            or "eventtypeid=91&" in pretty or "eventtypeid=505&" in pretty
            or "eventtypeid=39&" in pretty):
            return 'Men'
        if ("eventtypeid=82&" in pretty or "eventtypeid=3&" in pretty 
            or "eventtypeid=51&" in pretty or "eventtypeid=61&" in pretty
            or "eventtypeid=62&" in pretty or "eventtypeid=53&" in pretty 
            or "eventtypeid=71&" in pretty or "eventtypeid=11&" in pretty
            or "eventtypeid=67&" in pretty or "eventtypeid=504&" in pretty
            or "eventtypeid=68&" in pretty or "eventtypeid=64&" in pretty
            or "eventtypeid=506&" in pretty or "eventtypeid=63&" in pretty
            or "eventtypeid=92&" in pretty):
            return 'Women'
        if "eventtypeid=42&" in pretty:
            return 'Jr'
        if "eventtypeid=18&" in pretty:
            return 'UniMen'
        if "eventtypeid=19&" in pretty:
            return 'UniWomen'
        if "eventtypeid=83&" in pretty or "eventtypeid=4&" in pretty:
            return 'JrMen'
        if "eventtypeid=84&" in pretty or "eventtypeid=5&" in pretty:
            return 'JrWomen'
        if "eventtypeid=6&" in pretty:
            return 'SrMen'
        if "eventtypeid=7&" in pretty:
            return 'SrWomen'
        if ("eventtypeid=85&" in pretty or "eventtypeid=111&" in pretty
            or "eventtypeid=117&" in pretty or "eventtypeid=95&" in pretty):
            return 'MixedDoubles'
        if "eventtypeid=86&" in pretty or "eventtypeid=93&" in pretty:
            return 'Wheelchair'
        if "eventtypeid=8&" in pretty:
            return 'Combined'
        if "eventtypeid" in pretty:
            print(pretty[pretty.index("eventtypeid"):pretty.index("eventtypeid")+20])
        return 'Null'
        
@dataclass
class TeamsPage(Page):
    cz_event_id : int

    @property
    def url(self)->str:
        return 'https://curlingzone.com/event.php?eventid=%s&view=Teams#1'%(self.cz_event_id)
    
    @property
    def team_dict(self):
        pretty = self.soup.prettify()
        text = pretty.split('\n')
        teams = {}
        i = 0
        while i < len(text):
            while i < len(text) and 'wctlight_team_text' not in text[i]:
                i += 1
            i += 1
            if i < len(text):
                key = text[i].strip()
            while i < len(text) and 'Skip' not in text[i]:
                i += 1
            while i < len(text) and 'wctlight_player_text' not in text[i]:
                i += 1
            i += 1
            if i+2 < len(text):
                val = text[i].strip() + ' ' + text[i+2].strip()
                teams[key] = val
        #print(teams)
        return teams
    
    