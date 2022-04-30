## Example on how to do API calls to Meadows
## with OAuth2 / OpenID connect to get access
## to your own user data

## Client ID: "your.app.foo" You receive this from us.
## Client Secret: "YourSecret" You receive this from us.
## Redirect URI: URL of your app to for a GET callback with the 
##     Authorization Code. In the example we're using httpbin for simplicity.
## State: Optional. This will be forwarded back to your app.
## Scope: Optional. Not in use right now.

## Step 1. Ask end-user to authorize your app
## open a browser and navigate to the authorization page
xdg-open "https://meadows-research.com/oauth2/authorize?\
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

## Step 2. exchange Authorization Code for Access Token
curl -X POST \
-d 'grant_type=authorization_code' \
-d 'code=abc.def' \
-d 'client_id=your.app.foo' \
-d 'client_secret=YourSecret' \
https://meadows-research.com/oauth2/token

## This will print the json response, which should look something like:
# {"token_type": "Bearer", "access_token": "ghi.jkl", "expires_in": 86400.0}

## 3. Access protected page with access token
curl -i -H 'Accept: application/json' -H 'Authorization: Bearer ghi.jkl' https://meadows-research.com/users/jdoe
