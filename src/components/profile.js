import React, { useState, useEffect } from 'react';

const Profile = props => {
  const [profileState, setProfileState] = useState(props);
  console.log(profileState, props);

  useEffect(() => {
    setProfileState(props);
  }, [props]);

  return (
    <div>
      <p>
        <strong>Name:</strong>
        {profileState.name}
      </p>
      <p>
        <strong>Amount:</strong>
        {profileState.amount}
      </p>
      <button onClick={()=>console.log('add')}>+</button>
      <button onClick={()=>console.log('sub')}>-</button>
    </div>
  );
};



export default Profile;

