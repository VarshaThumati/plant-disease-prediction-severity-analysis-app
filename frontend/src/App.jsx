import { useState } from "react";
import ImageCapture from "./components/ImageCapture";
import ResultCard   from "./components/ResultCard";

// ── IMPORTANT: update this after deploying the backend to Render ──────────────
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/predict";

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result,       setResult]       = useState(null);
  const [loading,      setLoading]      = useState(false);
  const [error,        setError]        = useState(null);

  const handleImageSelected = (file) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);
  };

  const analyse = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(API_URL, { method: "POST", body: formData });
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Server error");
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Could not connect to the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      <header className="app-header">
        <span className="logo-leaf">🌿</span>
        <span className="logo-text">Plant Disease Detector</span>
      </header>

      <main className="app-main">

        <section className="card">
          <ImageCapture
            onImageSelected={handleImageSelected}
            disabled={loading}
          />

          {selectedFile && !loading && (
            <button className="btn-analyse" onClick={analyse}>
              Analyse leaf
            </button>
          )}

          {loading && (
            <div className="loading-row">
              <div className="spinner" />
              <span>Analysing image…</span>
            </div>
          )}

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}
        </section>

        {result && <ResultCard data={result} />}

      </main>

    </div>
  );
}
