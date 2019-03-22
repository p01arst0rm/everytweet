import os
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
        self.log_notify("..Existing manifest not found.")
        dict_list = glob.glob(str(self.dict_path))
        
        for f in dict_list:
            self.log_notify("building {}".format(f))
            
            dict_file = codecs.open(f, 'r', encoding='utf8').readlines()      
            manifest_dir =  self.tweet_manifest +"\\"+ f.split("\\")[-1]
            manifest_file = codecs.open(manifest_dir , 'w+', encoding='utf8')
            
            for line in dict_file:
                try:
                    a = self.prefix + line + self.suffix
                    manifest_file.write(a)
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

        # does a __manifest__ file exist? remove it.
        if os.path.isfile(self.tweet_manifest):
            os.remove(self.tweet_manifest)
            self.gen_manifest()
        
        # does a __manifest__ dir exist? add one.
        if not os.path.isdir(self.tweet_manifest):
            os.mkdir(self.tweet_manifest)
            self.gen_manifest()
        
        # is __manifest__ empty? build manifest.
        if glob.glob(str(self.tweet_manifest+"\\*")) == []:
            self.gen_manifest()

        self.manifest_files = glob.glob(str(self.tweet_manifest+"\\*"))

    def gen_tweet(self):
        while True:
            try:
                self.log_notify("fetching tweet..")
                with codecs.open(self.manifest_files[0], 'r', encoding='utf8') as f:
                    self.lines = f.readlines()
                    self.tweet = self.lines[0]
                    break
            except IndexError:
                self.log_warn("manifest file invalid!")
                os.remove(self.manifest_files[0])
                self.load_manifest()

    def rem_tweeted(self):
        self.log_notify("deleting tweeted line..")
        manifest = codecs.open(self.manifest_files[0], 'w', encoding='utf8')
        del self.lines[0]
        for line in self.lines:
            manifest.write(str(line))


    # main
    #----------------------------------------------------------------------------
    def run(self):
        # load manifest
        self.load_manifest()

        # generate tweet
        self.gen_tweet()
        
        # print tweet
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
        self.notify_log_file = ".\\everytweet.log"
        self.warn_log_file = ".\\everytweet.log"
        self.err_log_file = ".\\everytweet.log"

        self.prefix = ""
        self.suffix = ""

        self.dict = None
        self.tweet_manifest = ".\\__manifest__"
