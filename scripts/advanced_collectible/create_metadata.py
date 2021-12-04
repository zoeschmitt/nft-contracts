from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metada import metadata_template
from pathlib import Path
import requests
import json
import os


def main():
    advanced_collectible = AdvancedCollectible[-1]
    num_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {num_of_advanced_collectibles} collectibles!")
    for token_id in range(num_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete to overwrite.")
        else:
            print(f"Creating metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = "Puppy"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri


def upload_to_ipfs(filepath):
    # rb = open in binary
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # upload
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        res = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = res.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
