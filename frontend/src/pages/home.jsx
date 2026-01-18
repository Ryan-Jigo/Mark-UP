import "../../App.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import React from "react";
import History from "./history";
import Navbar from "../components/navbar";

function Home() {
    return (
        <div className="home">
            <Navbar />
            <div className="content">
                <h1>Welcome User,</h1>
                <p></p>
            </div>
            <History />
            <button className="new-btn">New +</button>
        </div>
    );
}
export default Home;