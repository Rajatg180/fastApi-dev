from sqlmodel import create_engine, Session, SQLModel

#url for database SQLite
DATABSE_URL = "sqlite:///./todo.db"

# echo true to see the sql statements in the terminal used to debugging and testing purpose
engine = create_engine(DATABSE_URL, echo=True)

# called once at the start of the application to create the datbase and tables 
# models must be imported before this function is called
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



# get a new session for interacting with the database
# this session is used to perform CRUD operations
# we are passing session as a dependency in our path operations

def get_session():
    with Session(engine) as session:
        yield session