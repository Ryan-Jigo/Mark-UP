import "../../App.css";

function New() {
    return (
        <div className="new-section">
            <h1>Create New Document</h1>
            <div className="new-card"><div className="course-input">
            <input type="text" placeholder="Course Name" />
            </div></div>
            <div className="new-card"><div className="batch-input"><input type="text" placeholder="Batch" /></div></div>
            <div className="new-card"><div className="exam-input"><input type="text" placeholder="Examination" /></div></div>
            <button className="upload-btn">Upload</button>
            <button className="create-btn">Create</button>
        </div>
    );
}
export default New;