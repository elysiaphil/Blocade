# Import the ERC721 interface
from vyper.interfaces import ERC721
tokenId: uint256 = 0  # Initialize tokenId with the value 0

# Define the contract
contract MyNFT(ERC721):

    # Constructor
    def __init__():
        ERC721.__init__()

    # Mint function to use generated NFTs
    @external
    def mint(address to, string memory ipfsUrl) external {
    tokenId++;  
    _mint(to, tokenId);
    _setTokenURI(tokenId, ipfsUrl);
}

    # Transfer function to transfer an NFT
    @external
    def transferNFT(from: address, to: address, tokenId: uint256):
        assert self._isApprovedOrOwner(from, tokenId)
        self._transfer(from, to, tokenId)

