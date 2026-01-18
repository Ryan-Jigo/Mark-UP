import "../../App.css";
import React from "react";
import ProfileAvatar from "../components/ProfileAvatar";
import Navbar from "../components/navbar";

function Profile() {
    return (
        <div className="profile-section">
            <Navbar />
            <h1>User Profile</h1>
            <div className="profile-layout">
                <div className="profile-icon" aria-label="Open profile">
                    <ProfileAvatar size={120} />
                </div>
                <div className="profile-content">
                    <div className="profile-card">
                        <div className="profile-info">
                            <label className="info-label">Name:</label>
                            <span className="info-value">ABCDEF</span>
                        </div>
                        <div className="profile-info">
                            <label className="info-label">Email:</label>
                            <span className="info-value">teacher@gmail.com</span>
                        </div>
                        <div className="profile-info">
                            <label className="info-label">ID:</label>
                            <span className="info-value">123456789</span>
                        </div>
                    </div>
                    <button className="edit-btn">Edit</button>
                </div>
            </div>
        </div>
    );
}

export default Profile;