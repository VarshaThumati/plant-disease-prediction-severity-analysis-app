import { useEffect, useRef } from "react";

function GaugeBar({ label, value, colorClass, hint }) {
  const barRef = useRef(null);

  useEffect(() => {
    // Animate bar from 0 → value after mount
    const bar = barRef.current;
    if (!bar) return;
    bar.style.width = "0%";
    const id = setTimeout(() => { bar.style.width = value + "%"; }, 50);
    return () => clearTimeout(id);
  }, [value]);

  const levelClass =
    value === 0     ? "level-none"   :
    value <= 35     ? "level-low"    :
    value <= 65     ? "level-medium" : "level-high";

  return (
    <div className="gauge-card">
      <div className="gauge-top">
        <span className="gauge-label">{label}</span>
        <span className={`gauge-value ${levelClass}`}>{value}%</span>
      </div>
      <div className="gauge-track">
        <div ref={barRef} className={`gauge-fill ${colorClass}`} style={{ width: "0%" }} />
      </div>
      {hint && <p className="gauge-hint">{hint}</p>}
    </div>
  );
}

export default function ResultCard({ data }) {
  if (!data) return null;
  const isHealthy = data.severity === 0;

  return (
    <div className="result-card">

      {/* Header */}
      <div className="result-header">
        <span className="result-icon">{isHealthy ? "✅" : "⚠️"}</span>
        <div>
          <h2 className="result-title">{data.plant} — {data.disease}</h2>
          <p className="result-sub">
            {isHealthy
              ? "No disease detected. Plant looks healthy."
              : `Detected with ${data.confidence}% model confidence`}
          </p>
        </div>
      </div>

      {/* Percentage gauges */}
      <div className="gauges">
        <GaugeBar
          label="Confidence"
          value={data.confidence}
          colorClass="fill-blue"
          hint="How certain the model is"
        />
        <GaugeBar
          label="Severity level"
          value={data.severity}
          colorClass="fill-amber"
          hint="Current disease intensity"
        />
        <GaugeBar
          label="Progression risk"
          value={data.progression}
          colorClass="fill-red"
          hint="Estimated spread likelihood"
        />
      </div>

      {/* Treatment */}
      <div className="treatment-box">
        <span className="treatment-icon">💡</span>
        <div>
          <p className="treatment-label">Recommended action</p>
          <p className="treatment-text">{data.treatment}</p>
        </div>
      </div>

      {/* Top 3 predictions */}
      <div className="top3-section">
        <p className="top3-title">Top predictions</p>
        {data.top3.map((item, idx) => (
          <div key={idx} className="bar-row">
            <div className="bar-label">
              <span className="bar-name">{item.label}</span>
              <span className="bar-pct">{item.confidence}%</span>
            </div>
            <div className="bar-track">
              <div
                className={`bar-fill ${idx === 0 ? "top" : ""}`}
                style={{ width: `${item.confidence}%` }}
              />
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
