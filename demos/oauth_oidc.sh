## Example on how to do API calls to Meadows
## with OAuth2 / OpenID connect to get access
## to your own user data

## open a browser and navigate to the authorization page
xdg-open meadows-research.com/authorize

## 2. this should trigger a GET to the client,
##    have to use external service to gather,
## 3. exchange auth token for access + refresh
curl meadows-research.com/authorize

## 4. access protected page with access token
curl meadows-research.com/users/jdoe
