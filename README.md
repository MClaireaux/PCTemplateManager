# BuildManager
 Software for computer builders, to track PC builds and computer pieces available in the inventory

The Build Manager has 3 functionnalities:
 - create a new build
 - get a quick accounting summary
 - add/update a computer part in the inventory

The inventory is a csv file located in ".\data\raw". See example from the "raw" folder

# MAIN MENU
The main menu shows:
 - The logo on the left
 - Access to the accounting summary and the inventory manager on the top right
 - A list of the builds already made on the middle right, with buttons to "open", "archive" or "delete" the build
 - A "Add new build" button at the bottom left

# CREATE A NEW BUILD
To create a new computer build, press the + button at the start menu. 
On the left is a draft, where the user can enter the name of pieces needed as well as an estimated price. Clicking on the button on the bottom left will automatically add all the prices and show the total price. The "suggested price" entry allows the  user to determine a total price him/herself.

On the right, the build menu allows the user to pick pieces that are marked as "In" in the Invenotry.csv file. The option menu "Type" shows all the type of computer parts present in the inventory (e.g. GPU, CPU, SSD...). One a Type is selected, the "Name " option menu will show all the parts corresponding to this Type that are available. 
The name of the parts are automatically combined with their ID (line number) to create unique names. Therefore, one piece cannot be selected in two different builds. This allows to easily plan when multiple computers are built at the same time.
Once a name is selected, the price at which it was bought appears automatically. 
The "Price sold" entry is for the user to fill with the price at which he wants to sell that piece. 
Clicking on the "Update" button next to "Final price" will sum the prices entered in the columns "Price" and "Price sold" to show a total. The "+10%" show the sum from the "Price" column, +10% margin. 
The "Final price" entry is for the user to fill.
Once the user is ready, he/she can give a name to the build and press the "Save" button on top. The values from the two menus are added to a "draft.csv" and "build.csv" file.

#OPEN AN EXISTING BUILD
From the main menu, click the first button in front of the name of the build you want to open. 
The program will access the "build.csv" and "draft.csv" files to recover the values you entered when you last saved that build.

#ARCHIVING A BUILD
When pushing the second button in front of a build's name in the main menu, the build will be moved from "build.csv" and "draft.csv" to "archive_build.csv" and "archive_draft.csv". 
The date at which it has been archived will be added automativally.
The name of the build will not appear in the main menu anymore. The only way to access that file is by opening in with ecel or another program.

#DELETING A BUILD
When pushing the third button in front of a build's name in the main menu, the build will be removed permanently.

# ACCOUNTING SUMMARY
The accounting summary is mainly based on the "Status" column of the inventory. The status can be "Ordered", "Sold", "In", or "cancelled".
The summary shows 
  - the total price of parts ordered (Amount ordered)
  - the total price of the parts in inventory (Amount in inventory)
  - the sum of the 2 previous amounts (Total exposure)
  - the total price at which the pieces were sold (Amount sold)
  - the total margin of the sells (sum of price sold - price bought)
Clicking on the down arrow shows the margin per PC build 

(!!! Note that it is not possible yet to mark pieces as part of a build and sold automatically. This functionnality is being added in the future !!!)

# MANAGING INVENTORY
Under construction, not functionnal yet


