# Components
## UI
**Initially, our idea was to have two different granularity options for the plug-in:**
- "Light Weight" fact checks integrated directly into the text via underlined passages, which, if you clock on them, reveal summarized information about the given statement and its correctness according to fact-checkers
- "Full Size" fact checks, which can be revealed and customized via a click on the plug-in icon

For more detail, please refer to the first wireframe prototype.

## Backend
**For now, there are only loose concepts for our backend realization, as there are many questions which need to be answered before we can get into detail.**

*Some aspects to be considered are:*
- We will need a system to evaluate the facts in texts/articles
	- Maybe we can use a Tag-based system
    - We also could try to track similarities across different texts
- A database will be needed to store the gathered information
	- Which DB-System will we use?
    - What should be stored in our database (URL, ID, whole text, tags only)?

## Frontend
**As this is planned to be a browser-extension, the frontend needs to be quite light**

- The extension needs the capability to share identifying aspects of the text/article with the server
	- The server should handle the gathering of the text which needs to be checked
    - How to deal with security?

- The extension needs to parse the fact-check information provided by the server
	- Needs capability to skim text in order to find the correct spot to insert fact-checker-comment


## Discarded Ideas
### Backend
- try to evaluate the reliability of the fact-checkers
	- Is this achievable through comparisons between different fact-checkers?
    - or we can do it throw reviews of the fact checkers.
    - or do it throw reporting false positives or false negatives
- make a list of the most popular news so we don't have to search the whole database for it.

