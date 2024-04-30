import React, { createContext, useContext, useState, useEffect } from 'react';
import { ethers } from 'ethers';

const WalletContext = createContext();

export const useWallet = () => useContext(WalletContext);

export const WalletProvider = ({ children }) => {
    const [walletAddress, setWalletAddress] = useState(null);
    const [balance, setBalance] = useState(0);

    const connectWallet = async () => {
        try {
            const provider = new ethers.BrowserProvider(window.ethereum);
            await provider.send('eth_requestAccounts', []);
            const signer = await provider.getSigner();
            const address = await signer.getAddress();
            setWalletAddress(address);
            fetchBalance(address);
        } catch (error) {
            console.error("Error connecting wallet:", error);
            alert("Failed to connect wallet. Please try again.");
        }
    };

    const fetchBalance = async (address) => {
        // Assuming you have an endpoint to fetch the balance
        const response = await fetch(`http://localhost:3000/balance/${address}`);
        if (response.ok) {
            const data = await response.json();
            setBalance(data.balance);
        } else {
            console.error("Error fetching balance:", response.statusText);
        }
    };

    useEffect(() => {
        if (walletAddress) {
            fetchBalance(walletAddress);
        }
    }, [walletAddress]);

    return (
        <WalletContext.Provider value={{ walletAddress, balance, connectWallet }}>
            {children}
        </WalletContext.Provider>
    );
};
