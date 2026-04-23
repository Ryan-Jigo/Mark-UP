import "../../App.css";
import { useNavigate } from "react-router-dom";
import { useState, useRef, useCallback } from "react";
import React from "react";
import Navbar from "../components/navbar";
import { uploadBatch, saveBatchLocally } from "../services/api";
import { FiUploadCloud, FiX, FiFileText, FiLoader } from "react-icons/fi";

function New() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [course, setCourse]     = useState("");
  const [batch, setBatch]       = useState("");
  const [date, setDate]         = useState("");
  const [exam, setExam]         = useState("");
  const [files, setFiles]       = useState([]);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading]   = useState(false);
  const [progress, setProgress] = useState([]);
  const [error, setError]       = useState("");

  const addFiles = (incoming) => {
    const images = Array.from(incoming).filter((f) => f.type.startsWith("image/"));
    setFiles((prev) => {
      const existing = new Set(prev.map((f) => f.name + f.size));
      return [...prev, ...images.filter((f) => !existing.has(f.name + f.size))];
    });
  };

  const removeFile = (index) => setFiles((prev) => prev.filter((_, i) => i !== index));

  const onDragOver  = useCallback((e) => { e.preventDefault(); setDragging(true); }, []);
  const onDragLeave = useCallback(() => setDragging(false), []);
  const onDrop      = useCallback((e) => { e.preventDefault(); setDragging(false); addFiles(e.dataTransfer.files); }, []);

  const handleCreate = async () => {
    setError("");
    if (!course.trim() || !batch.trim() || !date || !exam.trim()) {
      setError("Please fill in all fields.");
      return;
    }
    if (files.length === 0) {
      setError("Please upload at least one answer sheet image.");
      return;
    }
    setLoading(true);
    setProgress(files.map((f) => ({ name: f.name, status: "queued" })));

    const formData = new FormData();
    formData.append("course", course.trim());
    formData.append("batch",  batch.trim());
    formData.append("date",   date);
    formData.append("exam",   exam.trim());
    files.forEach((f) => formData.append("files", f));

    const timer = setInterval(() => {
      setProgress((prev) =>
        prev.map((p) => (p.status === "queued" ? { ...p, status: "processing" } : p))
      );
    }, 600);

    try {
      const result = await uploadBatch(formData);
      clearInterval(timer);

      // Reconstruct progress array based on the original files order
      const nextProgress = files.map((f, i) => {
        const rowNum = i + 1; // backend uses 1-indexed rows
        const student = result.students.find((s) => s.row === rowNum);
        const error = result.errors.find((e) => e.row === rowNum);

        if (student) {
          return {
            name: student.filename || f.name,
            status: "done",
            roll_no: student.roll_no,
            student_name: student.student_name,
            total_marks: student.total_marks,
          };
        } else if (error) {
          return {
            name: error.filename || f.name,
            status: "error",
            errorMsg: error.error,
          };
        }
        return { name: f.name, status: "error", errorMsg: "Unknown error" };
      });

      setProgress(nextProgress);

      if (result.students.length > 0) {
        saveBatchLocally({
          batch_id:      result.batch_id,
          course:        result.course,
          batch:         result.batch,
          date:          result.date,
          exam:          result.exam,
          student_count: result.student_count,
          students:      result.students,
          created_at:    new Date().toISOString(),
        });
        
        if (result.errors.length > 0) {
          setError(`Processed with ${result.errors.length} errors. Partial results saved.`);
        } else {
          setTimeout(() => navigate("/home"), 1000);
        }
      } else {
        setError("All uploads failed. Please check the errors below.");
      }
    } catch (err) {
      clearInterval(timer);
      setError(err.message || "Upload failed. Please try again.");
      setProgress((prev) => prev.map((p) => ({ ...p, status: "error", errorMsg: err.message })));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="new-section">
      <Navbar />

      {/* ── Page title ─────────────────────────────────────── */}
      <h1 className="new-page-title">Create New Document</h1>

      {/* ── Two-panel body ─────────────────────────────────── */}
      <div className="new-body">

        {/* LEFT – metadata cards stacked vertically */}
        <div className="new-left">
          <div className="meta-card">
            <span className="meta-icon">📘</span>
            <input
              className="meta-input"
              type="text"
              placeholder="Course Name"
              value={course}
              onChange={(e) => setCourse(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="meta-card">
            <span className="meta-icon">👥</span>
            <input
              className="meta-input"
              type="text"
              placeholder="Batch  (e.g. S4 AI-DS)"
              value={batch}
              onChange={(e) => setBatch(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="meta-card">
            <span className="meta-icon">📅</span>
            <span className="meta-label">Date</span>
            <input
              className="meta-input meta-input--date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="meta-card">
            <span className="meta-icon">📝</span>
            <input
              className="meta-input"
              type="text"
              placeholder="Examination  (e.g. IE1)"
              value={exam}
              onChange={(e) => setExam(e.target.value)}
              disabled={loading}
            />
          </div>
        </div>

        {/* RIGHT – drop zone + file list + buttons */}
        <div className="new-right">
          {/* Drop Zone */}
          <div
            className={`drop-zone ${dragging ? "drop-zone--active" : ""} ${loading ? "drop-zone--disabled" : ""}`}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => !loading && fileInputRef.current.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              style={{ display: "none" }}
              onChange={(e) => addFiles(e.target.files)}
            />
            <FiUploadCloud className="drop-zone-icon" />
            <p className="drop-zone-text">
              {dragging ? "Drop images here…" : "Click or drag answer sheet images here"}
            </p>
            <p className="drop-zone-sub">Supports JPG, PNG, JPEG</p>
          </div>

          {/* File Preview List */}
          {files.length > 0 && (
            <div className="file-list">
              {files.map((f, i) => {
                const prog = progress[i];
                return (
                  <div key={i} className="file-chip-wrapper" style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                    <div className={`file-chip ${prog ? `file-chip--${prog.status}` : ""}`}>
                      <FiFileText className="file-chip-icon" />
                      <span className="file-chip-name">{f.name}</span>
                      {prog?.status === "processing" && <FiLoader className="file-chip-spinner" />}
                      {prog?.status === "done" && (
                        <span className="file-chip-mark">✓ {prog.student_name || prog.roll_no || "Extracted"}</span>
                      )}
                      {!loading && (
                        <button
                          className="file-chip-remove"
                          onClick={(e) => { e.stopPropagation(); removeFile(i); }}
                          title="Remove"
                        >
                          <FiX />
                        </button>
                      )}
                    </div>
                    {prog?.status === "error" && prog.errorMsg && (
                      <span style={{ color: "#ef4444", fontSize: "12px", marginLeft: "12px" }}>
                        ⚠️ {prog.errorMsg}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* Error */}
          {error && <p className="new-error">{error}</p>}

          {/* Buttons */}
          <div className="new-actions">
            <button
              className="upload-btn"
              onClick={() => fileInputRef.current.click()}
              disabled={loading}
            >
              Upload Images
            </button>
            <button
              className="create-btn-inline"
              onClick={handleCreate}
              disabled={loading}
            >
              {loading ? "Processing…" : `Create${files.length > 0 ? ` (${files.length})` : ""}`}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

export default New;