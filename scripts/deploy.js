const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
    console.log("Memulai deployment EVotingHIMAFOR...");

    const ContractFactory =
        await hre.ethers.getContractFactory("EVotingHIMAFOR");

    const contract = await ContractFactory.deploy();

    await contract.waitForDeployment();

    const contractAddress = await contract.getAddress();
    const network = await hre.ethers.provider.getNetwork();

    const deploymentData = {
        contractName: "EVotingHIMAFOR",
        address: contractAddress,
        network: "localhost",
        chainId: Number(network.chainId)
    };

    const deploymentPath = path.join(
        __dirname,
        "..",
        "deployment.json"
    );

    fs.writeFileSync(
        deploymentPath,
        JSON.stringify(deploymentData, null, 4)
    );

    console.log("Deployment EVotingHIMAFOR berhasil!");
    console.log("Contract Address:", contractAddress);
    console.log("Chain ID:", Number(network.chainId));
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});