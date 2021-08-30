# ComputerDialog

## Props

<!-- @vuese:ComputerDialog:props:start -->
|Name|Description|Type|Required|Default|
|---|---|---|---|---|
|edit|The computer that we are editing if any has been given|`any`|`false`|-|
|dialog|The dialog that controls if this component is showing or not|`boolean`|`false`|-|

<!-- @vuese:ComputerDialog:props:end -->


## Methods

<!-- @vuese:ComputerDialog:methods:start -->
|Method|Description|Parameters|
|---|---|---|
|updated|Used to change the funcionalty from editing to new computer and vice versa|-|
|mounted|Used to open the component with the funcionalty of editing or new computer|-|
|handleProgram|Used to add a program to the computer programs list|The argument is a computer|
|deleteProgram|Used to remove a program to the computer programs list|The argument is a computer|
|close|Used to close this dialog|-|
|saveComputer|Used to save the newly created computer to the database making a call to the API or edit a given computer depending on the mode this component is working|The argument is a computer|
|deleteComputer|Used to remove a computer from the system|The argument is a computer|
|changeAllowed|Used to change the permissions of a user to allowed or disallowed|The first argument is a string representing the user who is to be changed The second argument is a boolean representing if the user is allowed(true) or not(false) The third argument is a string representing the mac of the computer that we want to allow access or not|

<!-- @vuese:ComputerDialog:methods:end -->


