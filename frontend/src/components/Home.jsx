import React from "react";
import "../assets/style.css"; // optional if you want consistent styling
import Header from "../Header/Header";

const Home = () => {
  return (
    <div>
      <Header />
      <div className="home-container">
        <h2>Welcome to Dealerships Portal</h2>
        <p>
          Explore car dealerships across different states, view details, and share your reviews.
        </p>
        <p>
          Use the navigation bar above to browse dealers or log in to post a review.
        </p>
      </div>
    </div>
  );
};

export default Home;

