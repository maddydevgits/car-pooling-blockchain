const carpool = artifacts.require("carpool");

module.exports = function (deployer) {
  deployer.deploy(carpool);
};
