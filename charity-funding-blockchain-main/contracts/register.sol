// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {
  
  bytes32[] _phonenos;
  bytes32[] _names;
  bytes32[] _places;
  address[] _wallets;


  function addUser(bytes32 phoneno,bytes32 name, bytes32 place, address wallet) public {
    _phonenos.push(phoneno);
    _names.push(name);
    _places.push(place);
    _wallets.push(wallet);
  }

  function viewUsers() public view returns(bytes32[] memory,bytes32[] memory,bytes32[] memory,address[] memory) {
    return (_phonenos,_names,_places,_wallets);
  }
}
