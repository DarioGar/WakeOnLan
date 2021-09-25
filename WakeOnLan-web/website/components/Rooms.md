# Rooms

View that handles the rooms on the system

## Methods

<!-- @vuese:Rooms:methods:start -->
|Method|Description|Parameters|
|---|---|---|
|event|Used to get set the programs that are going to be removed from a room|The first argument is a list of users to computersToRemove The second argument is the room from which the computers are going to be removed|
|swap|Used to swap the computers from the list of computers to be assigned to the room and free the computers from the list of computers to be freed from the roomd|The argument is a the room that will be changed|
|checkPermissions|Used to check the roles of the current user|-|
|getRooms|Used to get the rooms on the system|-|
|getComputersInRoom|Used to get the computers that are in the room|The argument is the room in which the computers are going to be searched|
|getComputersWithoutRoom|Used to get the computers that are not yet assigned to any room|-|
|saveRoom|Used to save a newly created room|-|
|deleteRoom|Used to delete a room|The argument is the room that will be deleted|

<!-- @vuese:Rooms:methods:end -->


