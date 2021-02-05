import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'react-router-dom';


const NameDisplay = () => {
    const [state, setState] = useState([]);

    useEffect(() => {
        axios.get(
          `http://localhost:5000/users`,
          console.log('trying to get user')
        )
        .then(response => setState(response.data), [])
        .catch(error => console.log(error));

        
    }, []);
    

    return (
      <div className="App">
        
        <ul>
            {
            state.map(user => (
                <li key={user.id}>
                    {user.name}
                    {user.amount}
                    <Link to={`/user/${id}`}>update amount</Link>
                </li>
            ))
            }
        </ul>
      </div>
    );
};

export default NameDisplay;