"""
Description: 
Queries the added profile information. Users can query only the profile information to which they have access.

Documentation:
https://docs.morelogin.com/l/en/interface-documentation/browser-profile#7_get_a_list_of_browser_profiles
"""

# pip install requests pycryptodome Crypto
from base_morelogin.base_func import requestHeader, postRequest

import sys
import asyncio
import traceback

# From profile list page, click on the API button, and copy API ID and API Key to below.
APPID = '1603184696627727'
SECRETKEY = '2a546deb503d4952abf0bd973d8d1e49'
BASEURL = 'http://127.0.0.1:40000'

async def main():
    try:
        data = await getEnvList(APPID, SECRETKEY, BASEURL)
        if len(data['dataList']) > 0:
            # Open profiles.txt in write mode, overwriting if it exists
            with open('profiles.txt', 'w') as f:
                for env in data['dataList']:
                    profile_info = f"{env['id']}: {env['envName']}\n"
                    f.write(profile_info)  # Write each profile to the file
            print('Profiles written to profiles.txt')
        else:
            print('No profile found, please check your condition')

    except:
        error_message = traceback.format_exc()
        print('Run error: ' + error_message)

# Get browser profile env list
async def getEnvList(appId, secretKey, baseUrl):
    requestPath = baseUrl + '/api/env/page'
    data = { 
        'pageNo': 1,                    # Env list page number
        'pageSize': 5,                  # Number of profiles per page
        'envName': '',                  # Env name condition for search
        # 'groupId': 123,                # Env group condition for search (optional)
    }
    headers = requestHeader(appId, secretKey)
    response = postRequest(requestPath, data, headers).json()

    if response['code'] != 0:
        print('Error: ' + requestPath + '\r\n' + response['msg'])
        sys.exit()

    return response['data']

if __name__ == '__main__':
    asyncio.run(main())
