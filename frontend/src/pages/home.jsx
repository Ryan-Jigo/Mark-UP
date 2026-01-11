import "../../App.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import React from "react";
import ProfileAvatar from "../components/ProfileAvatar";
import Settings from "../components/settings";
import History from "./history";

function Home() {
    return (
        <div className="home">
            <button className="profile-button" aria-label="Open profile">
                <ProfileAvatar size={32}/>
            </button>
            <button className="settings-button" aria-label="Open settings">
                <Settings size={32}/>
            </button>
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