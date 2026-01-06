import "../../App.css";
import React from "react";
import ProfileAvatar from "../components/ProfileAvatar";
import History from "./history";

function Home() {
    return (
        <div className="home">
            <button className="profile-button" aria-label="Open profile">
                <ProfileAvatar size={32}/>
            </button>
            <div className="content">
                <h1>Home Page</h1>
                <p></p>
            </div>
            <History />
            <button className="new-btn">New +</button>
        </div>
    );
}
export default Home;