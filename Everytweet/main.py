import sys
import glob
import tweepy
import ast
import codecs

class Everytweet:


    # Error handler
    #----------------------------------------------------------------------------
    
    def log_handle(self, log, log_file):
        print(log)
        with codecs.open(log_file, "a", encoding='utf8') as x:
            x.write(log + "\n")
           
    def log_notify(self, notif):
        self.log_handle(str("[INFO]: "+notif),self.notify_log_file)

    def log_warn(self, warn):
        self.log_handle(str("[WARNING]: "+warn),self.warn_log_file)

    def log_err(self, err):
        self.log_handle(str("[ERROR]: "+err),self.err_log_file)
        sys.exit()

           
    # Twitter handler
    #----------------------------------------------------------------------------
    
    def get_api(self):
        self.log_notify("Loading api..")
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)
        self.log_notify("..api loaded.")

    def publish_status(self):
        
        try:
            self.log_notify("Sending tweet..")
            if self.tweet.strip():
                self.api.update_status(status=self.tweet)
                self.log_notify("..tweet sent.")

        except tweepy.TweepError as e:
            # format dodgy returns from tweepy api
            err_dict_list = ast.literal_eval(e.response.text)

            # print errors
            for x in err_dict_list['errors']:
                self.log_err(str("{} ({})").format(x['message'],x['code']))

        except AttributeError:
            self.log_err("invalid tweet.")


    # tweet manifest parsing
    #---------------------------------------------------------------------------- 

    def gen_manifest(self):
        self.log_notify("building tweet manifest..")
        
        dict_list = glob.glob(str(self.dict_path))
        print(dict_list)

        for f in dict_list:
            tweet_dict = codecs.open(f, 'r', encoding='utf8').readlines()
            print(type(tweet_dict))
            manifest = codecs.open(self.tweet_manifest, 'a+', encoding='utf8')
            
            for line in tweet_dict:
                try:
                    a = self.prefix + line + self.suffix
                    manifest.write(a)

                except FileNotFoundError:
                    self.log_err("dictionary not found.")
                    sys.exit()
                
                except UnicodeDecodeError:
                    self.log_warn("could not decode line")
                    pass
                
                except:
                    self.log_err("could not build manifest.")
                    sys.exit()
                    
        self.log_notify("successfully built manifest.")
        
    def load_manifest(self):
        self.log_notify("loading tweet manifest..")
        
        try:
            codecs.open(self.tweet_manifest, 'r', encoding='utf8')
        except FileNotFoundError:
            self.log_notify("..Existing manifest not found.")
            self.gen_manifest()

    def gen_tweet(self):
        self.log_notify("generating tweet..")
        with codecs.open(self.tweet_manifest, 'r', encoding='utf8') as f:
            self.lines = f.readlines()
            self.tweet = self.lines[0]
    
    def rem_tweeted(self):
        self.log_notify("deleting tweeted line..")
        manifest = codecs.open(self.tweet_manifest, 'w', encoding='utf8')
        del self.lines[0]
        for line in self.lines:
            manifest.write(str(line))

    
    # main
    #----------------------------------------------------------------------------
    def run(self):
        # load manifest
        self.load_manifest()

        self.gen_tweet()
          
        self.log_notify(str("tweet: {}".format(self.tweet)))

        # get auth
        self.get_api()

        # send generated tweet
        self.publish_status()

        # delete tweeted line from manifest
        self.rem_tweeted()
          
    def __init__(self):
        self.api_key ="XXXXXXXXX"
        self.api_key_secret = "XXXXXXXXX"   
        self.access_token = "XXXXXXXXX"    
        self.access_token_secret = "XXXXXXXXX"

        self.dict_path = ""
        self.notify_log_file = "./everytweet.log"
        self.warn_log_file = "./everytweet.log"
        self.err_log_file = "./everytweet.log"

        self.prefix = ""
        self.suffix = ""

        self.dict = None
        self.tweet_manifest = "./manifest"
