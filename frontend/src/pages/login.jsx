import "../../App.css";
import { useNavigate } from "react-router-dom";
import {useState} from "react";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handlelogin = async () => {
    try {
      setError("");
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({email, password})
      });
      
      if (res.ok){
        const data = await res.json();
        // Store the token if needed
        localStorage.setItem("access_token", data.access_token);
        navigate("/home");
      } else {
        const errorData = await res.json();
        setError(errorData.detail || "Login failed");
      }
    } catch (err) {
      setError("Network error. Please check if the backend is running.");
    }
  }
  return (
    <div className="login">
      {/* Left text */}
      <div className="left">
        <h1>Mark UP</h1>
      </div>

      {/* Glass Login Card */}
      <div className="login-card">
        <h2>LOGIN</h2>

        {error && <div style={{color: 'red', marginBottom: '10px'}}>{error}</div>}

        <input 
          type="email" 
          placeholder="Email" 
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="signin-btn" onClick={handlelogin}>Sign in</button>
        
        <div className="links-container">
          <a href="#" className="signup-link">Sign up</a>
          <a href="#" className="forgot-password">Forgot Password?</a>
        </div>
      </div>
    </div>
  );
}

export default Login;
