import { useRef, useState } from "react";

/**
 * ImageCapture
 * Works on both desktop (file browser) and mobile (camera OR gallery).
 *
 * On mobile:
 *   "Take photo"  → opens rear camera directly (capture="environment")
 *   "From gallery"→ opens photo library (no capture attribute)
 *
 * On desktop:
 *   Both buttons open the OS file browser.
 *   Desktop browsers ignore the capture attribute safely.
 */
export default function ImageCapture({ onImageSelected, disabled }) {
  const cameraInputRef  = useRef(null);
  const galleryInputRef = useRef(null);
  const [preview, setPreview] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFile = (file) => {
    if (!file || !file.type.startsWith("image/")) return;
    const url = URL.createObjectURL(file);
    setPreview(url);
    onImageSelected(file);
  };

  // Drag-and-drop (laptop users)
  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const clearImage = () => {
    setPreview(null);
    onImageSelected(null);
    if (cameraInputRef.current)  cameraInputRef.current.value  = "";
    if (galleryInputRef.current) galleryInputRef.current.value = "";
  };

  return (
    <div className="capture-wrapper">

      {/* Hidden inputs */}
      <input
        ref={cameraInputRef}
        type="file"
        accept="image/*"
        capture="environment"          /* rear camera on mobile */
        onChange={(e) => handleFile(e.target.files[0])}
        style={{ display: "none" }}
      />
      <input
        ref={galleryInputRef}
        type="file"
        accept="image/*"               /* no capture = gallery / file browser */
        onChange={(e) => handleFile(e.target.files[0])}
        style={{ display: "none" }}
      />

      {!preview ? (
        /* ── Drop zone (shown before image selected) ── */
        <div
          className={`drop-zone ${dragOver ? "drag-over" : ""}`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
        >
          <div className="drop-icon">📷</div>
          <p className="drop-title">Upload or capture a leaf image</p>
          <p className="drop-sub">Drag and drop here, or use the buttons below</p>

          <div className="btn-row">
            <button
              className="btn-primary"
              onClick={() => cameraInputRef.current.click()}
              disabled={disabled}
            >
              Take photo
            </button>
            <button
              className="btn-secondary"
              onClick={() => galleryInputRef.current.click()}
              disabled={disabled}
            >
              Choose from gallery
            </button>
          </div>
        </div>
      ) : (
        /* ── Preview (shown after image selected) ── */
        <div className="preview-wrapper">
          <img src={preview} alt="Selected leaf" className="preview-img" />
          <button className="btn-clear" onClick={clearImage}>
            Change image
          </button>
        </div>
      )}
    </div>
  );
}
