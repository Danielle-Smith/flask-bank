import React, { Component } from 'react';
import NameDisplay from '../nameDisplay';


const Home = () => {
  
  
    return (
      <div className='app'>
        <h1>Bank</h1>
        {/* map users */}
        <h3>Kadence amount: $0</h3>
        <h3>Oliver amount: $0</h3>
        <h3>Gibson amount: $0</h3>
        {/* <UserDetails /> */}
        <p>-------</p>
        <NameDisplay/>
      </div>
    );
  
}
export default Home;