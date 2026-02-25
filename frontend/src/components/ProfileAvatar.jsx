import { FaUserCircle } from "react-icons/fa";
import "../../App.css";

function ProfileAvatar({size=32}) {
  return (
    <div className="profile-avatar glass">
      <FaUserCircle size={size} />
    </div>
  );
}

export default ProfileAvatar;
