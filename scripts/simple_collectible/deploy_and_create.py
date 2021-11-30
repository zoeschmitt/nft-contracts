from scripts.helpful_scripts import get_account,  OPENSEA_URL
from brownie import SimpleCollectible
sample_token_uri = "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png"


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    txn = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    txn.wait(1)
    print(f"Awesome, you can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    print("Please wait up to 20 min, and hit the refresh metadata button.")
    return simple_collectible

def main():
    deploy_and_create()