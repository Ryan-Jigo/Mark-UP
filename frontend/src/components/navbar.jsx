import { FaUserCircle } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import "../../App.css";
import ProfileAvatar from "./ProfileAvatar";
import Settings from "./settings";

const Navbar = () => {
    const navigate = useNavigate();
    return (
        <div className="navbar">
            <div className="navbar-left">
                <h1>Mark UP</h1>
            </div>
            <div className="navbar-right">
                <button className="navbar-icon-button profile-button" aria-label="Open profile">
                    <ProfileAvatar className="profile-avatar" onClick={() => navigate("/profile")} size={32}/>
                </button>
                <div className="profile" onClick={() => navigate("/profile")}>Profile</div>
                <button className="navbar-icon-button settings-button" aria-label="Open settings">
                    <Settings size={32}/>
                </button>
                <div className="Settings">Settings</div>
            </div>
        </div>
    )
}
export default Navbar;