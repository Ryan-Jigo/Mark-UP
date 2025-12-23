import "../../App.css";

function Login() {
  return (
    <div className="page">
      {/* Left text */}
      <div className="left">
        <h1>Mark <span className="up-text">UP</span></h1>
      </div>

      {/* Glass Login Card */}
      <div className="login-card">
        <h2>LOGIN</h2>

        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />

        <button className="signin-btn">Sign in</button>
        
        <div className="links-container">
          <a href="#" className="signup-link">Sign up</a>
          <a href="#" className="forgot-password">Forgot Password?</a>
        </div>
      </div>
    </div>
  );
}

export default Login;
