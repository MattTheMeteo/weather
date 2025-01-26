from onepassword.client import Client
from os import getenv
async def get_cds_api_key() -> str:
    # Get the service account path in OP
    svc = getenv('OP_SERVICE_ACCOUNT_TOKEN')
    if not svc:
        raise TypeError("OP_SERVICE_ACCOUNT_TOKEN is not set")
    # Auth to OP
    client =  await Client.authenticate(auth=svc, 
                                        integration_name="Green-Shoots-CDS",
                                        integration_version="1.0.0")
    val = await client.secrets.resolve("op://Green Shoots/CDSAPI/credential")
    return val
    
    