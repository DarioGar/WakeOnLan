# GroupList

## Methods

<!-- @vuese:GroupList:methods:start -->
|Method|Description|Parameters|
|---|---|---|
|mounted|Used to initialize data|-|
|roleColor|Used to get the user color based on their role|The argument is a string value representing the user role|
|getRooms|Used to get the rooms, retrieves all rooms and shows only the ones that are not occupied|-|
|getWorkGroup|Used to get the user's work groups if any, their members and room assigned|-|
|getGroupMembers|Used to get the members of a given group|The argument is a number indicating the ID of the group|
|roomAssigned|Used to get the room assigned to a given group|The argument is a number presesenting the group ID|
|checkPermissions|Used to check for the roles of the current user|-|
|close|Used to close the "New group" dialog|-|
|saveGroup|Used to save the newly created making a call to the API|-|
|deleteGroup|Used to delete a given group|The argument is a group|
|assignRoom|Used to assign a room to a group|The first argument is a room value representing the room that has to be assigned The second argument is a group value representing the group|
|deassignRoom|Used to deassign a room from a given group|The argument is a group|
|removeUserFromGroup|Used to remove a user from some group|The first argument is the user's username The second argument is a group The third argument is the index of that user in the group members list|

<!-- @vuese:GroupList:methods:end -->


