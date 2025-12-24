import "../../App.css";
import React from "react";
import ProfileIcon from "../components/ProfileIcon";
import History from "./history";

function Home() {
    return (
        <><div className="home">
            <div className="content">
                <h1>Home Page</h1>
                <p></p></div>
                <History />
            
            <button className="new-btn">New +</button>
        </div><button className="profile-button"><ProfileIcon /></button></>
    );
}
export default Home;