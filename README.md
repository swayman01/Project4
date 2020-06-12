# Project4
**CS50w Final Project**

## Why I developed this project:
Disruptions such as the COVID-19 pandemic result in local shortages, such as paper products. In these cases neighbors can help neighbors. Current avenues, such as Craigslist and Facebook Marketplace, are geared for shopping as opposed to focused needs. This app is designed to meet local community needs and not encourage shopping. Notice that the member has to "pull" based on a need rather than peruse. Notice also that there are no prices.

## How it Works:
### Membership Management
Prospective members apply using the sign-up form that populates the User model and associated Member\_profile model. Upon submission the app sends an email to the moderator (currently sent to the console, the system administrator needs to fill in details to send an actual email in production) and creates action items for all moderators. After the moderator checks the "Is approved" button in the Member\_profile model (moderators do not need to be superusers or have permission to modify the User model) the member can create Provisions and Needs.

If a member leaves the community, the app unchecks the member_profile "Is approved" button, unchecks the User model "Active" button, and converts all Open and Pending Needs and Provisions to "Retraced".
### Matching Needs and Provisions
The summary screen shows Active Needs and Provisions and Open Needs and Provisions. Members add new Needs, new Provisions, view their history, and edit their profile from here. They click on active needs and provisions to update them. They click on the Match Needs/Provisions buttons  to find matches. If they find an appropriate match they click on the Contact Info button for contact information for the matching person. After they contact the person, they update the status by clicking on one of the buttons at the bottom of the screen.

## Files
###  index.html, p4index.js, index(request) in views.py: 
**index.html** contains buttons for login and registration. **p4index.js** sets sessionStorage flags for visited\_login\_page and visited\_sign\_page to false. The reason is so that those pages aren't cluttered with error messages for a blank form.

**login.html** is a formatted version of the standard django file. p4login.js displays error messages. common.js contains functions used in more than one html file. One is a function for displaying errors and another converts JSON objects to javascript lists for sending to .html files.

The **password...reset** files are formatted version of the django versions.

### sign\_up.html, sign\_up.js, sign_up(request) in views.py:

These files allow the user to fill out the data for the django User model and custom Member\_profile model. The Member\_profile model houses data that isn't in the User model and a key to link them together. Upon completion of the form the app sends an email to the system administrator (console for development version) and creates an action item for moderators. Until the moderator approves the request, the user will get a message that says "you have not been approved" and their email on record (in case they typed it wrong). **forms.py** contains a simple checker **phone\_number\_checker(phone_number)** for the telephone number. It raises a validation error if there are not exactly 10 digits. When there are 10 digits, it strips away everything else and formats the number in dot notation. 

### summary.html, summary(request) in views.py:
These are the gateway to heart of the app. They display all of the members open items (provisions and needs) and active (those where a candidate member is identified but the transaction isn't closed). Moderators see their open action items and a full history of items The buttons at the top allow members to add new items, view all their items and edit their profile.

### format\_date(date_in) in views.py
This functions strips the time data and returns the Year, Month and Day.

### expiration\_due\_date\_check(request,provisions\_queryset,needs\_queryset) in views.py
This function checks to see if the expiration or due date is passed. If so, it changes the provision or need status to "Expiried".

### need\_form, provision\_form, p4need\_form.js, p4provision\_form.js, create\_need(request), create_provision(request) in views.py:
These format the django forms.

### need\_update\_form, provision\_update\_form, p4need\_form.js, p4provision_form.js:
These format the django update templates by getting rid of some clutter (help text and hh-mm-ss in the date fields). They also check that a pending item has a from or to member.

### all\_items.html, p4all\_items.js and all\_items(request,item_type) in views.py:
These files provide a formatted view of all of a member's needs and provisions including those that are fulfilled, expired, and retracted.


### action\_item.html, action\_item\_update\_item.html:
Moderators see their open action items on the summary.html page and an "Edit Action Item" button that allows them to update open action items. The "All Action Item" button shows all of their action items without edit capabilities. Only administrators can edit historical action items on the django admin site. 

### match\_provision.html, match\_need.html, match\_provision\_to\_need(request,pk,member\_id), match\_need\_to\_provision(request,pk,member\_id) in views.py:
These files search for candidate matching items that are "Open", "Available", or "Pending". They filter by type and look for common words They check the due date and expiration dates. The first section of the display has a list of candidate items with a button for the contact information. The second section has the desired item with an "Edit" button so that the member can modify it for better search results.

### provision\_contact\_info.html, need\_contact\_info.html, provision\_contact\_info(request,pk1,pk2), need\_contact\_info(request,pk1,pk2) in views.py.
These files provide the contact information so that the two members can decide if there is a match and make the exchange. There are four buttons to update the status (contact made, fulfilled, not a match, no longer able to fulfill).

### status\_update.html, and status\_update(request,pk1,pk2,pk3,pk4) in views.py:
These files allow members to update the status of their needs and provisions from the contact\_info screens.


### member\_profile\_update\_form and p4member\_profile\_update.js:
These files allow members to change their profile information, end their membership, or change their password. 

### end\_membership.html and end\_membership(request) in views.py:
These files allow members to terminate their membership. They set all open provisions and needs to "Retracted"; set their member\_profile.is\_approved and user.is\_active to False. Then they log the member out send them to a Sorry-to-See-You-Go screen.

### registration/logged\_out.html, p4logout.js, and logged_out(request) in views.py:
These files clear sessionStorage and log the members out.



