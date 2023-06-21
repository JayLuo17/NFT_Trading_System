from brownie import TitleToken, network
from metadata.metadata_sample import token_nft_template
from pathlib import Path
from input.user_inputs import NAME_LIST, input_dict
from scripts.help_scripts import get_account
import json, os, requests


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        f = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": f})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(f"The Title is wrapped in {file_uri}")
        return file_uri


def main():
    title = TitleToken[-1]
    number_of_titles = title.Counter()
    print(f"We have created {number_of_titles} titles!")

    for name in NAME_LIST:
        user_input = input_dict[name]

        # Prepare the metadata
        metadata = token_nft_template
        metadata["vehicle_id"] = user_input["vehicle_id"]
        metadata["token_status"] = user_input["token_status"]
        metadata["type"] = user_input["type"]
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{name}-{metadata['vehicle_id']}.json"
        )
        os.makedirs(os.path.dirname(metadata_file_name), exist_ok=True)
        with open(metadata_file_name, "w") as file:
            json.dump(metadata, file)
        if os.getenv("UPLOAD_IPFS") == "true":
            title_uri = upload_to_ipfs(metadata_file_name)

        # Create the title using the deployed contract
        account = get_account()
        creation_transaction = title.createNewTitle(title_uri, {"from": account})
        creation_transaction.wait(1)

        # Print all the data for future usage
        print(f"Created {name}'s vehicle title with id = {metadata['vehicle_id']};")
        print(
            f"The corresponding address is: {title.address} and the counter is {title.Counter() - 1}"
        )
        print(f"The token transaction address is {creation_transaction.txid}")
