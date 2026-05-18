import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Header.css";

const Header = () => {
  const navigate = useNavigate();
  const username = sessionStorage.getItem("username");

  const handleLogout = () => {
    sessionStorage.removeItem("username");
    navigate("/login");
  };

  return (
    <div className="header">
      <h2 className="logo">Dealerships</h2>
      <nav>
        <Link to="/home">Home</Link>
        <Link to="/about">About Us</Link>
        <Link to="/contact">Contact Us</Link>

        {!username ? (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        ) : (
          <>
            <span className="username">{username}</span>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </nav>
    </div>
  );
};

export default Header;
