"""Provide a check for aliveness for Viewer."""
from requests import get


def main(schema, host):
    """Convert an access attempt into an exit code for health check."""
    res = get("{}://{}/debug".format(schema, host))
    if res.status_code == 200:
        print("Success")
        exit(0)
    else:
        print("Non-200 exit code")
        exit(1)


if __name__ == "__main__":
    main(schema="http", host="localhost:5000")
