# fsi-23-bos-back-end


## Prerequisites 

- You will need to have Python installed.
- You will need administrative access on your machine for the virtual environment.
    - This is not required to run the program, but not having a virtual environment
    can lead to some issues.

## Installation 

Use the following command to locally install the Python dependencies to run the program. 

```pip install -r requirements.txt```


## Program Execution

Navigate to the server folder and use the following command.

```py server.py```

From there, the Flask server should be running and will be on your local machine. (Typically on http://127.0.0.1:5000)

## GraphQL Testing

Go to the address where your server is running on and go to `/graphql` (http://127.0.0.1:5000/graphql) to be able to test queries and gather results. 

## Creating Virtual Environment 
1. Allow scripts to run on your device 
    1. Run command prompt as administrator and enter powershell to start powershell
    2. use the command `Get-ExecutionPolicy` to view what permissions you have to run scripts on your device
    3. If your policy is `Restricted` or anything other than `AllSigned`, use the command `Set-ExecutionPolicy -ExecutionPolicy AllSigned` to allow scripts to be run on your device 

2. Install virtualenv by using the command `pip install virtualenv`

3. Create a virtual environment
    1. navigate to the root directory
    2. to create a directory called "venv", run the command `virtualenv venv`

4. `cd` to the root folder. Activate the virtual environment by running the commmand `.\\venv\Scripts\activate`. (venv) should appear at the begining of each command line

5. Install all packages by running `pip install -r requirements.txt`

6. Add venv/ to your `.gitignore` file so that venv/ does not get pushed to version control. **Every developer will have their own virtual environment on their own device.** 

## Virtual Environment 

1. Execute the program. If you get an error that a module is not installed, that means that module is not included in the `requirements.txt` file. Install the module by running `pip install <module>`. The script should show what version the module is, such as `requests-2.31.0`. Add the module into the requirements.txt file, and make sure the version matches the version you installed. 

## Installing Database Browser

In order for you to directly access the contents of the database, you will need to use 
**DB Browser for SQLite**

1. Install [DB Browser for SQLite](https://sqlitebrowser.org/). You can choose either the installation version
or portable version for use on USB Drives.
2. When you get the browser installed, click the option to `Open Database` in the 
top left corner. 
3. Navigate to the directory of the project and go to the `database` folder 
and click `database.db`

From there you should be able to explore different tables and their respective 
values and check whether the data is updating or is correct.