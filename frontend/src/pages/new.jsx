import "../../App.css";
import Navbar from "../components/navbar";

function New() {
    return (
        <div className="new-section">
            <Navbar />
            <div className="heading">
            <h1>Create New Document</h1></div>
            <div className="new-card"><div className="course-input">
            <input type="text" placeholder="Course Name" />
            </div></div>
            <div className="new-card"><div className="batch-input"><input type="text" placeholder="Batch" /></div></div>
            <div className="new-card"><label className="date-label">Select Date</label><div className="date-input"><input type="date"/></div></div>
            <div className="new-card"><div className="exam-input"><input type="text" placeholder="Examination" /></div></div>
            <button className="upload-btn">Upload</button>
            <button className="create-btn">Create</button>
        </div>
    );
}
export default New;