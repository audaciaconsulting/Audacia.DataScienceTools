import os
from dotenv import load_dotenv, find_dotenv

def get_env_var(variable: str):
    load_dotenv(find_dotenv())

    connection_string = os.environ.get(variable)

    if not connection_string:
        raise ValueError(
            f"{variable} not found in environment variables. "
            "Please check your .env file."
        )

    return connection_string