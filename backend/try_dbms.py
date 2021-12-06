import pyodbc


if __name__ == "__main__":
    # pyodbc connection string
    conn = pyodbc.connect("Driver={Amazon Redshift (x64)}; "
                          "Server=redshift-cluster-1.c26kfcowhljw.us-west-1.redshift.amazonaws.com; "
                          "Database=covid_19; UID=awsuser; PWD=Mark29013; Port=5439")

    # Define Cursor
    cus=conn.cursor()

    # Execute SQL statement to get current datetime and store result in cursor
    cus.execute('select sex, count(*) as count from c_19_cases group by sex;')

    # Display the content of cursor
    row = cus.fetchall()

    print(row)