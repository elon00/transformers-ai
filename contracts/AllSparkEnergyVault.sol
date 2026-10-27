// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AllSparkEnergyVault
 * @dev Cybertron Autonomous Morphic Compute & AllSpark Energy Protocol
 */
contract AllSparkEnergyVault {
    address public supremeCommander; // Optimus Prime
    uint256 public allSparkEnergonReserve;
    enum MorphicMode { VEHICLE, ROBOT, FLIGHT }
    MorphicMode public currentSystemMode;

    struct AutobotUnit {
        string designation;
        uint256 energonAllocation;
        MorphicMode mode;
        bool isActive;
    }

    mapping(address => AutobotUnit) public autobots;

    event MorphicTransition(address indexed autobot, MorphicMode fromMode, MorphicMode toMode);
    event EnergonTransferred(address indexed recipient, uint256 amount);
    event AllSparkInfused(uint256 amount);

    constructor() {
        supremeCommander = msg.sender;
        allSparkEnergonReserve = 5_000_000_000 ether;
        currentSystemMode = MorphicMode.ROBOT;
    }

    modifier onlyCommander() {
        require(msg.sender == supremeCommander, "Only Supreme Commander Optimus Prime");
        _;
    }

    function registerAutobot(address unitAddress, string memory name, uint256 energon) external onlyCommander {
        require(allSparkEnergonReserve >= energon, "Energon depleted");
        allSparkEnergonReserve -= energon;

        autobots[unitAddress] = AutobotUnit({
            designation: name,
            energonAllocation: energon,
            mode: MorphicMode.ROBOT,
            isActive: true
        });

        emit EnergonTransferred(unitAddress, energon);
    }

    function transformMorphicState(MorphicMode newMode) external {
        AutobotUnit storage bot = autobots[msg.sender];
        require(bot.isActive || msg.sender == supremeCommander, "Unauthorized unit");

        MorphicMode oldMode = bot.mode;
        bot.mode = newMode;
        emit MorphicTransition(msg.sender, oldMode, newMode);
    }
}
