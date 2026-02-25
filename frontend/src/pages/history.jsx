import "../../App.css";
import React from "react";

function History() {
    const historydata=[
        {id:1,exam:"IE1", name:"DS",batch:"S4 AI-DS", date:"2024-06-01"},
        {id:2,exam:"IE2", name:"AAD",batch:"S6 CS-AI", date:"2024-05-28"},
        {id:3,exam:"IE1", name:"SE", batch:"S2 CS-AI ", date:"2024-05-20"},          
    ]
    return (
        <div className="history-section">
            {historydata.map((item)=>(
                <div key={item.id} className="history-card">
                    <h3>{item.name}</h3>
                    <p>{item.batch}</p>
                    <p>{item.exam}</p>
                    <p>{item.date}</p>
                    <button className="download-btn">Download</button>
                </div>
            ))}
        </div>
    );
}
export default History;