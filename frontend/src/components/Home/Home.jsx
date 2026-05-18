import React from "react";
import Header from "../Header/Header";
import "../assets/style.css"; // optional for consistent styling

const Home = () => {
  return (
    <div>
      <Header />
      <div className="home-container">
        <h2>Welcome to Dealerships Portal</h2>
        <p>Browse dealers, filter by state, and post reviews once logged in.</p>
      </div>
    </div>
  );
};

export default Home;
