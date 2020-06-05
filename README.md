# Project4
CS50w Final Project
1. Why I developed this project
   Disruptions such as the COVID-19 pandemic can result in local shortages, such as paper products. In these cases neighbors can help neighbors. Current avenues, such as Craigslist and Facebook Marketplace are geared for shopping as opposed to focus needs. This site is setup to meet focused needs and not encourage shopping. Notice that the member has to "pull" based on a need rather than peruse. Notice also that there is no prices.
2. How it Works
 A. Membership Management
Prospective members apply using the signup form that populates the User model and associated Member_profile model. Upon submission the app sends an email to the moderator (currently sent to the console (the system administrator needs to fill in details to send a real email in production) and created action items for all moderators. After the moderator checks the "Is approved" button in the Member_profile model (moderators do not need to be superusers or have permission to modify the User model) the member can create Provisions and Needs.
 If a member decides to leave the community, the app unchecks the member_profile "Is approved" button, unchecks the User model "Active" button, converts all Open and Pending Needs and Provisions to "Retracted".
 B. Matching Needs and Provisions
3. Other
   History
