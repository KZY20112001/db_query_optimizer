# Initialising the database

This will initialise a dockerized instance of the PostgreSQL database with TPC-H on a windows machine.

## Prerequisites:

-   [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)

## Initial setup:

1.  For custom set up, you can copy your `.tbl` files to the `tbls` directory (the default files are provided for convenience)
   
2.  Run the cleaning script to generate the `.csv` files.

    ```
    $ python read_tbls.py
    ```

3.  Start the PostgreSQL database up by running the docker image.

    ```
    $ docker compose up
    ```

4.  When the containers are up, initialise the database by running the initialisation batch script. This should take around 5-6 minutes.

    ```
    $ ./init_database.bat
    ```

-   If you delete the containers, you will have to rerun the initial setup steps again.

## Interacting with database using pgAdmin

You can view that the database has been correctly generated and also query the database using pgAdmin

1. Go to `http://localhost:5050` on your web browser
1. Login with the following credentials

    - username: `admin@admin.com`
    - password: `admin`

1. Create new server
    - Create “TPC-H" as server name under General -> Name
    - Under Connection:
        - Change address to `pg_container`
        - Change Username to `postgres`
        - Set Password to `admin`
1. Click on "Save".
1. You can now interact with the Database, check `TPC-H -> Databases -> tpch -> Schemas -> Public -> Tables`. You can use the query editor by right clicking and using the Query Tool.
1. You should be able to access pgAdmin and the PostgreSQL database should be preserved between sessions.
