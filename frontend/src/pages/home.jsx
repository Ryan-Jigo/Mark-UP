import "../../App.css";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import React from "react";
import History from "./history";
import Navbar from "../components/navbar";
import { getLocalBatches } from "../services/api";

function Home() {
  const navigate = useNavigate();
  const [batches, setBatches] = useState([]);

  // Reload from localStorage whenever this page is focused
  useEffect(() => {
    const load = () => setBatches(getLocalBatches());
    load();
    window.addEventListener("focus", load);
    return () => window.removeEventListener("focus", load);
  }, []);

  return (
    <div className="home">
      <Navbar />
      <div className="content">
        <h1>Welcome, Teacher</h1>
        <p className="home-sub">
          {batches.length === 0
            ? "You have no documents yet. Create one with the button below."
            : `${batches.length} document${batches.length !== 1 ? "s" : ""} processed`}
        </p>
      </div>
      <History batches={batches} />
      <button className="new-btn" onClick={() => navigate("/new")}>New +</button>
    </div>
  );
}

export default Home;