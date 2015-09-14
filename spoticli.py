import string
import random
import json
import requests
import re
import ssl
import sys, getopt


# Default port that Spotify Web Helper binds to.
PORT = 4371

class SpotifyCLI(object):
    oauth_token = None
    csrf_token = None

    def setup(self):
        self.domain = '{0}.spotilocal.com'.format(
            ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        )
        #changed url endpoints
        self.oauth_token = self.get('https://embed.spotify.com/remote-control-bridge/')
        self.csrf_token = self.get('/simplecsrf/token.json')['token']

    def get(self, url, params={}, headers={}):
        response = ""
        isCSRF = False
        
        if url.startswith('/'):
            url = "https://%s:%d%s" % (self.domain, PORT, url)
            isCSRF = True

        # Always add the default parameters and headers
        params.update({
            'oauth': self.oauth_token,
            'csrf': self.csrf_token,
        })
        #headers also needed to be changed
        headers.update({
            'Referer':'https://embed.spotify.com/remote-control-bridge/',
            'Origin': 'https://embed.spotify.com/'
        })
        
        #SSL verification is currently set to false because Im currently unable to figure out why its refusing the certificate
        request = requests.get(url, params=params, headers=headers, verify=False)
        
        if isCSRF:
            response = request.json()
        else:
            data = request.text
            search = re.compile('(?<=a = \')(.*)(?=\';)')
            parsed = search.findall(data)
            response = parsed[0]
            
        return response  
        

    def get_status(self):
        return self.get('/remote/status.json')

    def playpause(self):
        status = self.get_status()
        if status.get('playing') is True:
             self.pause()
        else:
             self.unpause()

    def pause(self, pause=True):
        return self.get('/remote/pause.json', {'pause': json.dumps(pause)})

    def unpause(self):
        return self.pause(pause=False)

    def play(self, spotify_uri):
        return self.get('/remote/play.json', {
            'uri': spotify_uri,
            'context': spotify_uri
        })

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "", ["play=","pause","unpause","skip_forward","skip_back","status","playpause"])
    except getopt.GetoptError:
        print "Usage: spoticli.py --play=<uri>|--pause|--unpause|--skip_forward|--skip_back"
        sys.exit(2)
    for opt, arg in opts:
        print opt
        if opt == "--play":
            spotify.play(arg)
        elif opt == "--pause":
            spotify.pause()
        elif opt == "--unpause":
            spotify.unpause()
	elif opt == "--playpause":
	    spotify.playpause()
        elif opt == "--skip_forward":
            print "Haven't implemented yet"
        elif opt == "--skip_back":
            print "Haven't implemented yet"
	elif opt == "--status":
	    print spotify.get_status()

if __name__ == '__main__':
    spotify = SpotifyCLI()
    spotify.setup()
    main(sys.argv[1:])
    
