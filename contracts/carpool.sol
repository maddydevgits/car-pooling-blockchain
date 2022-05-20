// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract carpool {
  
  // state variables
  address[] _drivers;
  string[] _cartype;
  uint[] _counts;
  uint[] _rideid;
  uint[] _minAmount;
  string[] _from;
  string[] _to;

  function createRide(address driver,string memory cartype,uint count,uint rideid,uint minAmount,string memory from, string memory to) public  {

    _drivers.push(driver);
    _cartype.push(cartype);
    _counts.push(count);
    _rideid.push(rideid);
    _minAmount.push(minAmount);
    _from.push(from);
    _to.push(to);

  }

  function viewRides() public view returns (address[] memory, string[] memory,uint[] memory,uint[] memory,uint[],string[] memory,string[] memory) {
    return (_drivers,_cartype,_counts,_rideid,_minAmount,_from,_to);
  }
}
