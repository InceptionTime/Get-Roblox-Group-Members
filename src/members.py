import requests
import csv

GROUP_ID = 1  # Add group id
RANK_NAME = 'RANK NAME'  # Add rank name


def Send_Request(endpoint):
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }
    try:
        response = requests.get(endpoint, headers=headers)
    except ConnectionError as e:
        print(f"Request Connection Error:\n{e}")
    except TimeoutError as e:
        print(f"Request Timeout:\n{e}")
    except Exception as e:
        print(f"Something went wrong sending the request\n{e}")
    else:
        if response.status_code == 200:
            json = response.json()
            return json
        else:
            print(f"Status code:\n{response.status_code} - {endpoint}")
            return None


def Get_Role_From_Group(role_name):
    Roles = Send_Request(
        f"https://groups.roblox.com/v1/groups/{GROUP_ID}/roles")

    for role in Roles['roles']:
        if role_name in role['name']:
            return role['id']
    return None


def main():
    # Update string to role name
    ROLE_ID = Get_Role_From_Group(RANK_NAME)
    if ROLE_ID == None:
        print("Role not found")
        return

    Users = Send_Request(
        f"https://groups.roblox.com/v1/groups/{GROUP_ID}/roles/{ROLE_ID}/users?limit=100&sortOrder=Asc")

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "User ID"])
        for user in Users['data']:
            writer.writerow([user['username'], user['userId']])

        while Users['nextPageCursor'] != None:
            for user in Users['data']:
                print(user)
                writer.writerow([user['username'], user['userId']])
            Users = Send_Request(
                f"https://groups.roblox.com/v1/groups/{GROUP_ID}/roles/{ROLE_ID}/users?limit=100&sortOrder=Asc&cursor={Users['nextPageCursor']}")
        print("Done")


main()
