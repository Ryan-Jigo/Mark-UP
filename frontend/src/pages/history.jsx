import "../../App.css";
import React from "react";

function History() {
    const historydata=[
        {id:1,exam:"IE1", name:"S4 Mech", date:"2024-06-01"},
        {id:2,exam:"IE2", name:"S2 Civil", date:"2024-05-28"},
        {id:3,exam:"IE1", name:"S4 Civil", date:"2024-05-20"},
        {id:4,exam:"IE2", name:"S3 Electrical", date:"2024-05-15"},           
    ]
    return (
        <div className="history-section">
            {historydata.map((item)=>(
                <div key={item.id} className="history-card">
                    <h3>{item.name}</h3>
                    <p>{item.exam}</p>
                    <p>{item.date}</p>
                    <button className="download-btn">Download</button>
                </div>
            ))}
        </div>
    );
}
export default History;