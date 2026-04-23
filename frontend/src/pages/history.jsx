import "../../App.css";
import React, { useState, useEffect } from "react";
import { downloadResult } from "../services/api";
import { FiDownload, FiFileText, FiAlertCircle } from "react-icons/fi";

function History({ batches = [] }) {
  const [downloading, setDownloading] = useState(null);
  const [dlError, setDlError]         = useState(null);

  const handleDownload = async (b) => {
    setDlError(null);
    setDownloading(b.batch_id);
    try {
      const filename = `${b.course}_${b.batch}_${b.exam}_${b.date}.xlsx`;
      await downloadResult(b.batch_id, filename);
    } catch (err) {
      setDlError(`Download failed: ${err.message}`);
    } finally {
      setDownloading(null);
    }
  };

  if (batches.length === 0) {
    return (
      <div className="history-empty">
        <FiFileText size={48} style={{ opacity: 0.35 }} />
        <p>No documents yet. Click <strong>New +</strong> to create one.</p>
      </div>
    );
  }

  return (
    <div className="history-section">
      {dlError && (
        <div className="dl-error">
          <FiAlertCircle /> {dlError}
        </div>
      )}

      {batches.map((b, idx) => (
        <div key={b.batch_id || idx} className="history-card">
          {/* Left: info */}
          <div className="hcard-info">
            <h3>{b.course}</h3>
            <div className="hcard-badges">
              <span className="badge badge--batch">{b.batch}</span>
              <span className="badge badge--exam">{b.exam}</span>
            </div>
            <p className="hcard-meta">
              {b.date} &nbsp;·&nbsp; {b.student_count ?? b.students?.length ?? 0} student{(b.student_count ?? b.students?.length ?? 0) !== 1 ? "s" : ""}
            </p>
          </div>

          {/* Right: download */}
          <button
            className="download-btn"
            onClick={() => handleDownload(b)}
            disabled={downloading === b.batch_id}
          >
            {downloading === b.batch_id ? (
              "Downloading…"
            ) : (
              <>
                <FiDownload style={{ marginRight: 6 }} />
                Download
              </>
            )}
          </button>
        </div>
      ))}
    </div>
  );
}

export default History;