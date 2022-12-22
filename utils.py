import boto3

session = boto3.Session(profile_name='coms6156')
SSM_CLIENT = session.client('ssm')


def get_google_ouath_keys() -> dict:
    """Retrieve secrets from Parameter Store."""

    parameters = SSM_CLIENT.get_parameters(
        Names=[
            "ORGANIZERS_MICROSERVICE_GOOGLE_CLIENT_ID",
            "ORGANIZERS_MICROSERVICE_GOOGLE_CLIENT_SECRET",
        ],
        WithDecryption=True,
    )

    keys = {}
    for parameter in parameters["Parameters"]:
        keys[parameter["Name"]] = parameter["Value"]

    return (
        keys["ORGANIZERS_MICROSERVICE_GOOGLE_CLIENT_ID"],
        keys["ORGANIZERS_MICROSERVICE_GOOGLE_CLIENT_SECRET"],
    )
