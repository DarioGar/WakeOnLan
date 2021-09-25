# UserTable

Handles the users on the system, the funcionality allowed depends on the user's role

## Methods

<!-- @vuese:UserTable:methods:start -->
|Method|Description|Parameters|
|---|---|---|
|checkAdminRole|Used to check if the current user has the admin role|-|
|mounted|Used to initialize the component|-|
|sendInvite|Used to send an invitation to a user|The first argument is a string representing the name of the user invited The second argument is a number representing the group ID the invitation is for|
|getWorkGroup|Used to get the groups the user is a member of|-|
|getUsers|Used to get the list of users on the system|-|
|editItem|Used to initialize the form with the user selected data so it can be edited|The argument is a user|
|deleteItem|Used to open the dialog the confirm deletion|The argument is a user|
|deleteItemConfirm|Used to confirm the deletion of a user|-|
|deleteUser|Used to delete a user|The argument is a strign representing the user's username|
|close|Used to close the dialog for a new|editing user|-|
|closeDelete|Used to deny the deletion of a user|-|
|saveUser|Used to save a newly created user or to update a current user|-|

<!-- @vuese:UserTable:methods:end -->


