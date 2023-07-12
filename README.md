# fsi-23-bos-back-end


## Prerequisites 

- You will need to have Python installed.

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
    a. Run command prompt as administrator and enter powershell to start powershell
    b. use the command "Get-ExecutionPolicy" to view what permissions you have to run scripts on your device
    c. If your policy is "Restricted" or anything other than "AllSigned", use the command "Set-ExecutionPolicy -ExecutionPolicy AllSigned" to allow scripts to be run on your device 

2. Install virtualenv by using the command "pip install virtualenv"

3. Create a virtual environment
    a. navigate to the root directory
    b. to create a directory called "venv", run the command "virtualenv venv"

4. Add venv/ to your .gitignore file so that venv/ does not get pushed to version control. Every developer will have their own virtual environment on their own device. 

## Virtual Environment 

1. Cd to the root folder. Activate the virtual environment by running the commmand ".\\venv\Scripts\activate". (venv) should appear at the begining of each command line

2. Install all packages by running "pip install -r requirements.txt"

3. Execute the Program. If you get an error that a module is not installed, that means that module is not included in the requirements.txt file. Install the module by running "pip install <module>". The script should show what version the module is, such as requests-2.31.0. Add the module into the requirements.txt file, and make sure the version matches the version you installed. 
