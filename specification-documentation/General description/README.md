# General Introduction

The idea behind Archicheck is to have an architecture that allows users to view and publish critical comments or remarks about the content of any given
website in the World Wide Web they're currently on. These comments can either come from other users or already established fact-checking sites you can subscribe to.
By subscribing to different fact-checking sites (e.g. [correctiv.org](https://correctiv.org/)), the user has the opportunity to compare their stated facts and check them for potential inequalities. 

We will try to realize Archicheck via a web extension/plug-in which displays an overview of existing comments that can be toggled on and off. Furthermore we want to turn every browser into a fact-checking webserver to hold something against the monopoly of the big tech corporations and their algorithms.

# Features
- Subscribe to *arbitrary* "fact checkers" and publish fact checks &#8594; see use cases

- Repost tracker
    - in order to check facts, a repost tracker could be used to find where some information came up first, and whether we trust that site or not determines what to make of that information. if the source finding is not that easy the repost tracker could also be just a way of identifying URLs that dont need to be fact checked again
- ~~Tags~~
  - Has been discarded because a site using the same keywords can still have a totally different attitude towards the topic e.g. we need vaccines, and vaccines are going to kill us all have the same keyword vaccine but they should be treated different.
- Give institutions (e.g. press agencies) a special status
    - relay their fact checks
    - subscribe to those by default
- optional: Use Machine Learning to score new information based on their similarity to something press agencies you subscribe to have published
- optional: Not only link URLs containing the actual fact checking content, but publish the content itself via comment that the user can enter in a text field

# Roles
## Role 1: Recipient of fact checks
For this role, login credentials are **not** required, because we can store the subscribed fact checkers locally.

### use case 'getting fact checks for a URL'
- user (for this section, i.e. the recipient of fact checks) is surfing on website that should be fact-checked (hash of the URL of the website works as identifier)
- there are three possible settings for this use case:

    1. "explicit-request-mode"
       - user click on plugin icon, which opens a list of fact-checks for this URL
          - request to "fact check source" (peer-to-peer network/the server)
                  - GET request to "serverAdress/hashedURLtoFactCheck/factchecker_id
                  - later, also allow sending a list of multiple fact-checkers that the recipient has subscribed to
                  - if the recipient simply wishes to access *all* fact checks for this URL, we no not specify the factchecker_id in the request: `GET serverAdress/hashedURLtoFactCheck/` and get back a factchecker_ids, that have published fact checks for this URL
          - entries of this list are
              -  the user name of the fact checker in the p2p network/on the server
              -  the HTML `title` tags of the website containing the fact check
              - entries from press agencies that are subscribed to by default
          - each entry works as hyperlink to the content of the fact check
              - this means, the fact check itself is hosted on a website and we only need to store the assignment (URL **to** fact-check &#8594; URL **of** the fact check, fact checker user name)
      - list entry will be greyed out when clicking on the corresponding link
          - saving this information in internal data base (e.g. indexedDB)
    2. "daemon-mode"
       - like "explicit-request-mode", but the extension is requesting fact checks automatically for every visited URL.
       - if there are fact checks available for the current URL, the plugin icon is being modified to show the number of available fact checks
       - it is possible to exclude websites from these automatic requests in the settings
    3. "disabled"
       - the extension does not send any requests until entering any of the other modes


### use case 'adding a new subscription to a fact checker'
- user clicks on plugin icon
- user clicks on `Add fact checker`-button
- user enters an identifier ("user name") or the public key fingerprint that they want to subscribe to
- verify, if that fact checker exists in the network
    - if so, new subscription written to internal data base
    - otherwise an error message will be shown

### use case 'install plugin'
- user installs extension in the way specified for the specific browser
- on first click on the plugin icon there is a prompt "Do you wish to see the Usage Guide?" with a link tohttps://github.com/clecap/archicheck/blob/main/narrative-description/user%20guide.md

### use case 'unsubscribe a fact checker'
- user clicks on plugin icon
- user clicks on 'subscribed fact checkers'-button which opens a list of the subscribed fact checkers
- user clicks on 'unsubscribe'-button next to the fact checker they want to unsubscribe
- notification 'Are you sure you want to unsubscribe?' appears
- user clicks 'yes'-button
- fact checker is removed from the list


## Role 2: Publisher of fact checks (aka "fact checker")

### use case 'create account'
- user opens browser extension
- user clicks on publish a new fact check( or my published fact checks)
- the app will give the user the option to login or sign up
- the user clicks on sign up
- application prompts for user name, email and password(and confirm) that is stored to DB
- key pair is generated and stored to local DB
- public key is published to server component alongside with the username

- (optional: allow to verify your credibility of for example by showing you are autor at XYZ)

### use case: 'login' (for registered fact checkers)
- user opens browser extension
- user clicks on publish a new fact check( or my published fact checks)
- if the user is not signed in, an option with login will appear.
- the user clicks on login and enters his username and password.

### use case: 'change password'
- user clicks on my account.
- user clicks on change password.
- user has to confirm the old password and insert the new password.

### use case: 'change username'
- user clicks on my account.
- user clicks on change username.
- user insert the new username.

### use case 'publish a new fact check'
- user (who has an existing user account) is surfing on website
- user clicks on plugin icon
- user clicks on 'add fact check for this website'-button
- user enters a URL containing the fact check
- when finished, user clicks on 'add fact check'-button
- HTML `head` of that URL containing the fact check, the URL that has fact checked and the corresponding user name is broadcast to P2P network so that subscribers can access this information when requesting fact checks for a certain URL from a certain "fact checker"
- this means, that fact checks in our network are triples of the URL to check, the URL _containing_ the fact check and the user who created this fact check (plus the usual, such as timestamp of publication)

### use case 'delete a fact check'
- publisher clicks on plugin icon "my published fact checks" which opens a list of fact checks this user has already published
- user clicks on 'delete'-button next to the comment he wants to delete
    - of course users can only delete their own comments
- notification 'Are you sure you want to delete this comment?' appears
- user clicks 'yes'-button
- comment is removed from the list
- N.B.: the published fact checks should be cryptographically signed anyway to prove the authenticity, so we can simply use the "revoke certificate" mechanism for marking deleted fact checks


