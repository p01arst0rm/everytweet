from Everytweet import Everytweet

app =Everytweet()

app.dict_path = "./dictionaries/*"
#app.dict_path = "./dictionaries/english.txt"

app.prefix = "did you know that "
app.suffix = " is an english word?"

app.api_key ="XXXXXXXXXXXXXXXXXXXXXXXXX"        
app.api_key_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
app.access_token = "XXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
app.access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

app.run()