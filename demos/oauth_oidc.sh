## Example on how to do API calls to Meadows
## with OAuth2 / OpenID connect to get access
## to your own user data

##TODO: replace domain with https://meadows-research.com

## open a browser and navigate to the authorization page
xdg-open "https://staging.meadows-research.com/oauth2/authorize?\
client_id=your.app.foo&\
redirect_uri=https://httpbin.org/get&\
state=xyz&\
scope=test"

## After submitting the form with the correct login details,
## you should see the httpbin page displaying the plain request data,
## starting with something like:
# {
#   "args": {
#     "code": "abc.def", 
#     "state": "xyz"
#   }, 

## 2. exchange auth token for access + refresh
curl -X POST \
-d 'grant_type=authorization_code' \
-d 'code=abc.def' \
-d 'client_id=your.app.foo' \
-d 'client_secret=YourSecret' \
https://staging.meadows-research.com/oauth2/token

## This will print the json response, which should look something like:
# {"token_type": "Bearer", "access_token": "ghi.jkl", "expires_in": 86400.0}

## 3. access protected page with access token
curl -H 'Authorization: Bearer ghi.jkl' https://staging.meadows-research.com/users/jdoe

