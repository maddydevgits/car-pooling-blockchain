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
  string[] _places;
  string[] _dates;

  uint[] _tripids;
  address[] _bidders;
  string[] _bidplaces;
  uint[] _bidamounts;
  bool[] _bidstatus;

  function createRide(address driver,string memory places,string memory cartype,uint count,uint rideid,uint minAmount,string memory from, string memory to,string memory _date) public  {

    _places.push(places);
    _drivers.push(driver);
    _cartype.push(cartype);
    _counts.push(count);
    _rideid.push(rideid);
    _minAmount.push(minAmount);
    _from.push(from);
    _to.push(to);
    _dates.push(_date);

  }

  function viewRides() public view returns (address[] memory, string[] memory,string[] memory,uint[] memory,uint[] memory,uint[] memory,string[] memory,string[] memory,string[] memory) {
    return (_drivers,_places,_cartype,_counts,_rideid,_minAmount,_from,_to,_dates);
  }

  function bidRide(uint tripid, address bidder, string memory place, uint bidamount) public {

    _tripids.push(tripid);
    _bidders.push(bidder);
    _bidplaces.push(place);
    _bidamounts.push(bidamount);
    _bidstatus.push(false);
  }

  function viewBids() public view returns(uint[] memory,address[] memory, string[] memory, uint[] memory,bool[] memory) {
    return (_tripids,_bidders,_bidplaces,_bidamounts,_bidstatus);
  }

  function acceptBid(uint tripid, address bidder) public {

    uint i;
    for(i=0;i<_tripids.length;i++) {
      if(_tripids[i]==tripid && _bidders[i]==bidder) {
        _bidstatus[i]=true;
      }
    }
    for(i=0;i<_rideid.length;i++) {
      if(_rideid[i]==tripid) {
        _counts[i]--;
      }
    }
  }
}
