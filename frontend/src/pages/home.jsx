import "../../App.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import React from "react";
import History from "./history";
import Navbar from "../components/navbar";

function Home() {
    const navigate = useNavigate();
    return (
        <div className="home">
            <Navbar />
            <div className="content">
                <h1>Welcome User,</h1>
                <p></p>
            </div>
            <History />
            <button className="new-btn" onClick={()=>navigate("/new")}>New +</button>
        </div>
    );
}
export default Home;