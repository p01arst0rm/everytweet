from Everytweet import Everytweet

app =Everytweet()

app.dict = "./dictionaries/english.txt"
app.modifier = "test "
             
app.api_key ="XXXXXXXXXXXXXXXXXXXXXXXXX"        
app.api_key_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
app.access_token = "XXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
app.access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
app.run()