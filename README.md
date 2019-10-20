How to install working version on your laptop:

FIRST: Clone the repository onto your PC.

SETUP PYTHON DEVELOPMENT TOOLS

    1. Download PyCharm IDE (https://www.jetbrains.com/pycharm/) and open the git project in it.
    2. Download and install Anaconda 3 on your computer (https://docs.anaconda.com/anaconda/install/)
        - You will need to install a couple of packages that do not come with the anaconda distribution; 
        depending on your preferences you can either use Anaconda or pip to install the packages. 
        We recommend using Anaconda since it is the most easiest for now (https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html#installing-packages).
        - Packages that you need to install include:
            -flask, apscheduler, falsk-restful and pandas
            -the command line comanads to install these packages are: "conda install flask","conda install -c conda-forge apscheduler","conda install flask-restful",
            "conda install pandas"
            -you will also need to install the packages in pycharm idea in order to import them(file->settings->project:flaskapp->project interpreter->here you click on '+' to install all the packages)
    3. Start the app by running the app.py file. The Flask server will be starting under http://127.0.0.1:5000/.
       - Possible errors include:
            1. You did not install all packages correctly. Check the command line which package is not defined and 
            needed and use Anaconda to install the missing package
            2. You did not set the project interpreter to be your Anaconda distribution. 
            To solve this you need to set it in PyCharm -> Preferences->Project:flaskapp -> Project Interpreter 
            -> Choose Anaconda distribution -> Apply (this may take a while)
    4. The Flask Application is now successfully running. You can test the API using Postman or any other tool of your 
    liking. The app will also print a string every 10 seconds in the console. This is a scheduler which will have further
    functionalities in the future. Verify that he is working correctly as well.
