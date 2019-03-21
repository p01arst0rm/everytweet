import sys
import glob
import tweepy
import ast


class Everytweet:

    # Error handler
    #----------------------------------------------------------------------------
    
    def log_handle(self, log, log_file):
        print(log)
        with open(log_file, "a") as x:
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
        self.log_notify("building tweet manifest...")
        self.log_notify("please choose a dictionary:\n")
        
        i = 0
        self.dicts = glob.glob(self.dict_dir + "*.txt")
        while i < len(self.dicts):
            print("[{}] {}".format(i, self.dicts[i].split("\\")[1]))
            i = i + 1
        
    def load_manifest(self):

        try:
            self.log_notify("loading existing tweet manifest...")
            self.tweet_manifest = open('tweet_manifest_dir', 'r')
        except FileNotFoundError:
            self.log_notify("..Existing manifest not found.")
            self.tweet_manifest = self.gen_manifest()

    # main
    #----------------------------------------------------------------------------
    def run(self):
        # load manifest
        self.transcripts = self.load_manifest()


          
        # generate a tweet from the text model
        #self.gen_tweet()

        # get auth
        #self.get_api()
          
        # send generated tweet
        #self.publish_status()

          
    def __init__(self):
        self.api_key ="XXXXXXXXX"
        self.api_key_secret = "XXXXXXXXX"   
        self.access_token = "XXXXXXXXX"    
        self.access_token_secret = "XXXXXXXXX"

        self.notify_log_file = "./everytweet.log"
        self.warn_log_file = "./everytweet.log"
        self.err_log_file = "./everytweet.log"

        self.dict_dir = "./dictionaries/"
        self.tweet_manifest_dir = "./manifest"
        self.suffix_mode = False

if __name__ == '__main__':
    app = Everytweet()
    app.run()
