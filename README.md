### Setting up the database:

This process can be skipped if you already have the PostgreSQL server running with the relevant data loaded.

1. Ensure Docker is installed. 
2. Set up the database by following the instructions inside [`db/README.md`](db/README.md)



### Running the program

1. Install virtual environment by running 

    ```pip install virtualenv```

2. Create a virtual environment by running

    ```python -m venv .venv```

3. Activate the virtual environment by running

    Windows: `.venv\Scripts\activate`

    Unix/macOS: `source .venv/bin/activate`

4. Install required dependencies

    ```pip install -r requirements.txt```


5. Start the program in the root folder by running

    ```python project.py```

6. If you followed the database set-up above, you can use the password `admin` to connect to the database server (the other fields will be pre-filled). If you are using your own server, fill in the relevant details and connect to the server. 

7. For testing, you can use the sample queries in `test_queries` folder. 
