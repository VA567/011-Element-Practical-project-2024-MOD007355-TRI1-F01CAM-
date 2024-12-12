###Importing Libraries###
import datetime #This allows me to get the current date and time
from netmiko import ConnectHandler as ch #This allows me to connect to the remote computer and enter linux commands from python
import socket #This allows me to get the IP address of the user
import requests #This allows me to get the code from web a specific web page
import sys #This allows me to cleanly exit the program

###Main Menu Function###
def MainMenu():
    #Creating the main menu dictionary
    mainMenuDictStr = {"1." : "Show date and time .......... (Local Computer)",
                       "2." : "Show IP address ............. (Local Computer)",
                       "3." : "Show home directory listing . (Remote Computer)",
                       "4." : "Backup file ................. (Remote Computer)",
                       "5." : "Save web page ............... (Local Computer)",
                       "Q." : "Quit"}
    
    #Printing the menu
    print("\n#####-Main Menu-#####\n")
    #This for loop will iterate through all the items in the mainMenuDictStr, and it will print the key with its corresponding value
    for x, y in mainMenuDictStr.items():
            print(x, y)
    print("\n")

###User Selection###
def UserInput():
    while True:
        UserSelection = input("Please select an option from the menu, e.g. 1 for option one and q for quit: ").lower()

        if UserSelection == "1":
            showDateAndTime()
            break

        elif UserSelection == "2":
            showIpAddress()
            break

        elif UserSelection == "3":
            showHomeDirectory()
            break

        elif UserSelection == "4":
            remoteFileBackup()
            break

        elif UserSelection == "5":
            saveWebPage()
            break

        elif UserSelection == "q" or UserSelection == "quit":
            print("\nQuitting...\n")
            sys.exit(0)
        else:
            print("\n- Please select a number between 1 and 5 or q to quit\n")

###Command Functions###
#NetMiko Configuration Function
def netMikoConfig():
    print("\nRunning NetMiko Configuration\n")

    #The net_connect variable needs to be declared as a global variable so it can be called in other functions
    global net_connect

    while True:
        print("##########################-Running NetMiko Configuration-##########################")
        try:
            net_connect = ch(
                #The device_type variable stores the type of operating system that you are trying to connect to
                device_type = input("Please enter the type of operating system on your remote computer, e.g. linux :").lower(),

                #The host variable stores the IP address of the computer that you are trying to connect to
                host = input("Please enter the remote IP address, e.g. 192.168.1.106 :"),

                #The port variable stores the port number you are trying to connect through
                port = input("Please enter the port you would like to establish a connection through, e.g. 22 :"),

                #The username variable stores the username of the account on the computer you are trying to connect to
                username = input("Please enter the username of the remote computer:"),

                #The password variable stores the password of the account on the computer you are trying to connect to
                password = input("Please enter the password of the remote computer:")
            )

            #These lines of code are needed to test if the user entered valid Netmiko configuration settings
            net_connect.send_command("ls")

            print("\nNetmiko Setup Completed Successfully")

            break

        except:
            print("\n- An error occurred, please ensure that you have entered the correct details\n")


#Option 1 - Showing the date and time of the local computer
def showDateAndTime():
    print("\nShowing the date and time of the local computer")

    #The following 2 lines of code use the datetime library.
    dateAndTime = datetime.datetime.now() #This line gets the current date and time
    formattedDateAndTime = dateAndTime.strftime("%Y-%m-%d %H:%M") #This line of code formats the date and time, removing the milliseconds

    print(formattedDateAndTime)

    input("\nPress enter/return to continue: ")

#Option 2 - Showing the IP address of the local computer
def showIpAddress():
    print("\nShowing the IP Address of the local computer")

    #gets the host name of the user's computer through the socket library
    hostNameStr = socket.gethostname()
    #gets the host's ip address by using the host name variable
    hostIpAddress = socket.gethostbyname(hostNameStr)

    #this prints the host name and the ip address of the user's computer
    print(f"\n- The host name of your computer is: {hostNameStr} \n- The IP Address of your computer is: {hostIpAddress}")

    input("\nPress enter/return to continue: ")

#Option 3 - Output the home directory listing of a remote computer
def showHomeDirectory():
    print("\nShowing home directory listing")

    #Calling the NetMiko Configuration function
    netMikoConfig()

    #If the command in the try statement fails the except statement will catch the error
    try:
        #The cd command changes the directory and the .. moves one directory up in the hierarchy
        command = "cd .."
        #Sends the command cd .. to the remote computer. The expect_string variable tells netmiko to expect a $ symbol in the output
        net_connect.send_command(command, expect_string=r"$")


        #The command ls lists all the files and folder in the current directory
        command = "ls"
        #Sends the command ls to the remote computer
        output = net_connect.send_command(command)

        #The output variable currently has three lines stored within it. This line of code splits each line and arranges it in list
        output = output.splitlines()

        #Outputs the second item in the output list. It has the directory listing of the home directory stored within it
        print(f"\n{output[1]}")

    except:
        #This is only printed when try statement fails
        print("Command Failed")

    finally:
        print("\nDisconnecting...")
        #Disconnects netmiko from the remote computer freeing up more of the computer's resources
        net_connect.disconnect()

        input("\nPress enter/return to continue: ")

#Option 4 - Backup a file on a remote computer
def remoteFileBackup():
    print("\nBacking up a file")

    #Calling the netmiko configuration function
    netMikoConfig()

    while True:
        #Asks the user to input the file path of the filed they'd like to back up
        filePath = input("\nEnter the file path of the file you would like to back up:")

        #If the file path is invalid the except command will catch the error and prompt the user to enter a valid file path
        try:
            #The cp command copies the file path the user entered and creates a new file with .old suffix added to the end
            command = f"cp {filePath} {filePath}.old"
            #Sends the command to the virtual machine and runs it in the terminal. The output does not need to be saved to a variable.
            net_connect.send_command(command)

            #Lets the user know the backup completed successfully
            print("Backup complete")
            break

        except:
            #This is only printed when the user mistypes the file path
            print("Please enter a valid file path, e.g /home/victor/textfile.txt")

        finally:
            #disconnects from the virtual machine
            net_connect.disconnect()

    input("\nPress enter/return to continue: ")

#Option 5 - Save a web page as a text file
def saveWebPage():
    print("\nSaving a web page")

    #Loops the code when the URL is invalid
    while True:
        # Asks the user to enter the URL of the webpage they'd like to download and what they'd like to name the downloaded file
        websiteURL = input("\nPlease enter the URL of the webpage you'd like to download: ")
        filename = input("Please enter the name you'd like to associate with your file: ")

        try:
            #This line of code gets the web page's contents and saves it to the variable
            webContent = requests.get(websiteURL)

            contentText = webContent.text

            #The with statement automatically closes the open function.
            #The encoding uft-8 tells the open function to use Unicode. If utf-8 encoding is not selected it will result in an error.
            #The only downside is the file is only made when the app closes
            with open(f"{filename}.txt", "w", encoding="utf-8") as file:
                #Writes the web page's contents to the file
                file.write(contentText)

            print("\nFile Saved")
            break

        except:
            #Lets the user know that an error occurred
            print("\nFile Saved Unsuccessfully")
            print("Please check the URL entered was correct and valid\n")

    input("\nPress enter/return to continue: ")


###Calling the Functions###
while True:
    MainMenu()
    UserInput()