# ShappList

<br />
<br />


Current to-do list (first steps to get going):
 * [ ] Home page to define main design/colors/style (bootstrap from the get go)(Create differences between Desktop and mobile from the get go to define a standard for the rest of the project);
 * [ ] Define DB Tables;
 * [ ] Take a look at the android browser container app;
 * [ ] Create Auth system with token system;
 * [ ] Create example shopping list;

<br />
<br />

Development Notes:
 * All Javascript and CSS should be kept on single files on the static folder (try not to code js and css on the actual html pages).
 * Dont use the template features of Django, as it will make it easier to change to Node later on.
 
<br />
<br />

Software/Utilities to be used:
  * Backend server (as of now) - Django;
  * DB Server - MySQL;
  
<br />
<br />

Services:
  * API.
  * Authentication.
  * Main App.
  * Admin Panel.
  * Statistics Services to work along side admin panel.
  
<br />
<br />


### Authentication:

<br />

Auth Notes:
 * Tokens should last 12h (fine tune it later);  

<br />
<br />

### Shopping List related:

<br />

Shopping List notes:
  * Restrictions should be either Open (anyone can edit list), closed (only owner can edit list) or whitelisted (check SL_Whitelist for who is allowed to edit list);


<br />
<br />

### Databases:
<br />

#### users
| user_id       | username      | password |
| :-----------: |:-------------:| :-------:|
|-|-|-|


<br />

#### users_extended (not finished, only create until later)
| user_id       | email        |
| :-----------: |:-------------:|
|-|-|

<br />

#### tokens_table
| user_id       | token_date      | token |
| :-----------: |:-------------:| :-------:|
|-|-|-|

<br />

#### sl_groups
| group_id       | name      | owner_id | restrictions |
| :-----------: |:-------------:| :-------:|:-------:|
|-|-|-|-|

<br />

#### sl_whitelist
| group_id       | user_id        |
| :-----------: |:-------------:|
|-|-|

<br />

#### user_groups
| group_id       | user_id        |
| :-----------: |:-------------:|
|-|-|
