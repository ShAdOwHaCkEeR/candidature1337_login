import requests
from bs4 import BeautifulSoup
from dependency_injector import containers, providers

class Login(object):

    def __init__(self, username, password) -> None:
         
         self.username = username
         self.password = password

         self.session = requests.session()
         self.param = ""
         self.token = ""

         self.parser = 'lxml'
         self.links_ = {
            'base_url': 'https://candidature.1337.ma/users/sign_in',
            'meetings': 'https://candidature.1337.ma/meetings'
         }

         self.data = {}

         self.valid = False
         self.chkin_available = False

    @property
    def param_(self) -> str:
        return self.param
    
    @param_.setter
    def param_(self, value: str):
        self.param = value

    @property
    def token_(self) -> str:
        return self.token

    @token_.setter
    def token_(self, value: str):
        self.token = value

    @property
    def valid_(self) -> bool:
        return self.valid

    @valid_.setter
    def valid_(self, value: bool):
        self.valid = value

    @property
    def chkin_available_(self) -> bool:
        return self.chkin_available

    @chkin_available_.setter
    def chkin_available_(self, value: bool):
        self.chkin_available = value
    
class AuthClient(Login):

    def __init__(self, username, password) -> None:
        super().__init__(username, password)

    def __ScrapeToken(self) -> None:

        # get authenticity_token
        r_ = self.session.get(
            url=self.links_['base_url']
        )
        soup = BeautifulSoup(r_.text, self.parser)
        
        self.param_ = soup.find('meta', {'name': 'csrf-param'})['content']
        self.token_ = soup.find('meta', {'name': 'csrf-token'})['content']

    def connect(self) -> None:

        # initialize post data/payload
        self.data['utf8'] = "✓"
        self.data[self.param] = self.token
        self.data['user[email]'] = self.username
        self.data['user[password]'] = self.password
        self.data['commit'] = "Se connecter"

        r_ = self.session.post(
            url=self.links_['base_url'],
            data=self.data
        )

        # validation
        self.valid_ = (r_.url == self.links_['meetings'])
        if self.valid:
            self.chkin_available = "New &#39;check-ins&#39;" not in r_.text

    def run(self) -> None:

        self.__ScrapeToken()
        self.connect()

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    Client = providers.Singleton(
        AuthClient, 
        username = config.username,
        password = config.password
    )