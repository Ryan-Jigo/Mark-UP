import "../../App.css";
import React from "react";
import { FaCog } from "react-icons/fa"

function Settings({OnClick}) {
    return (
        <FaCog size={28} onClick={OnClick} className="settings-icon" aria-label="Open settings"/>
    );
}
export default Settings;

            