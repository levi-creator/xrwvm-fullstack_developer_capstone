import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  // Fetch all dealers initially
  const get_dealers = async () => {
    const res = await fetch("/djangoapp/get_dealers/All", { method: "GET" });
    const retobj = await res.json();
    if (retobj.status === 200) {
      const all_dealers = Array.from(retobj.dealers);
      const statesList = [...new Set(all_dealers.map(dealer => dealer.state))];
      setStates(statesList);
      setDealersList(all_dealers);
    }
  };

  // Fetch dealers filtered by state
  const filterDealers = async (state) => {
    const url = `/djangoapp/get_dealers/${state}`;
    const res = await fetch(url, { method: "GET" });
    const retobj = await res.json();
    if (retobj.status === 200) {
      setDealersList(Array.from(retobj.dealers));
    }
  };

  // Load dealers on first render
  useEffect(() => {
    fetch("https://kiptoolevi-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/djangoapp/get_dealerships")
      .then(response => response.json())
      .then(data => {
        console.log("Fetched dealers:", data);
        setDealersList(data.dealers);
      })
      .catch(error => console.error("Error fetching dealers:", error));
  }, []);
  


  const isLoggedIn = sessionStorage.getItem("username") != null;

  return (
    <div>
      <Header />
      <table className='table'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select
                name="state"
                id="state"
                onChange={(e) => filterDealers(e.target.value)}
              >
                <option value="" disabled hidden>State</option>
                <option value="All">All States</option>
                {states.map(state => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
        <tbody>
          {dealersList.map(dealer => (
            <tr key={dealer.id}>
              <td>{dealer.id}</td>
              <td><a href={`/dealer/${dealer.id}`}>{dealer.full_name}</a></td>
              <td>{dealer.city}</td>
              <td>{dealer.address}</td>
              <td>{dealer.zip}</td>
              <td>{dealer.state}</td>
              {isLoggedIn && (
                <td>
                  <a href={`/postreview/${dealer.id}`}>
                    <img
                      src={review_icon}
                      className="review_icon"
                      alt="Post Review"
                    />
                  </a>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dealers;
