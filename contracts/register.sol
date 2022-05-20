// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {

  // state variables
  address[] _usernames;
  string[] _names;
  string[] _emails;
  string[] _mobiles;
  string[] _passwords;

  function registerUser(address username,string memory name,string memory email, string memory mobile,string memory password) public {

    _usernames.push(username);
    _names.push(name);
    _emails.push(email);
    _mobiles.push(mobile);
    _passwords.push(password);
  }

  function viewUsers() public view returns (address[] memory,string[] memory,string[] memory,string[] memory,string[] memory) {
    return (_usernames,_names,_emails,_mobiles,_passwords);
  }

  function compare(string memory _a, string memory _b) private pure returns (bool) {
        bytes memory a = bytes(_a);
        bytes memory b = bytes(_b);
        uint minLength = a.length;
        if (b.length < minLength) minLength = b.length;
        //@todo unroll the loop into increments of 32 and do full 32 byte comparisons
        for (uint i = 0; i < minLength; i ++)
            if (a[i] < b[i])
                return false;
            else if (a[i] > b[i])
                return false;
        if (a.length < b.length)
            return false;
        else if (a.length > b.length)
            return false;
        else
            return true;
    }

  function loginUser(address username,string memory password) public view returns (bool) {
    
    uint i;

    for(i=0;i<_usernames.length;i++) {
    
      if(username==_usernames[i] && (compare(password,_passwords[i]))){
        return true;
      }
    }
    return false;
  }

}
