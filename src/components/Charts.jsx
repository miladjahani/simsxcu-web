import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Charts = ({ chartData, selectedOption }) => {
  if (!chartData || chartData.length === 0) {
    return (
      <div className="card">
        <h2>نمودارها</h2>
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          پس از انجام شبیه‌سازی، نمودارها در اینجا نمایش داده خواهند شد
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>نمودارهای شبیه‌سازی</h2>
      
      <div className="grid grid-2">
        <div style={{ height: '300px' }}>
          <h4>رابطه v/v% با ML و AML</h4>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="v_v_percent" label={{ value: 'v/v%', position: 'insideBottom', offset: -5 }} />
              <YAxis label={{ value: 'g/l Cu', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="AML" stroke="#8884d8" name="AML" strokeWidth={2} />
              <Line type="monotone" dataKey="ML" stroke="#82ca9d" name="ML" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ height: '300px' }}>
          <h4>بار آلی و راندمان استخراج</h4>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="v_v_percent" label={{ value: 'v/v%', position: 'insideBottom', offset: -5 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="loaded_organic" stroke="#ff7300" name="Loaded Organic" strokeWidth={2} />
              <Line type="monotone" dataKey="extraction_efficiency" stroke="#387908" name="Extraction Efficiency %" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {selectedOption === 2 && (
        <div style={{ height: '300px', marginTop: '20px' }}>
          <h4>پارامترهای کارخانه</h4>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="v_v_percent" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="ML" stroke="#8884d8" name="Maximum Loaded" />
              <Line type="monotone" dataKey="loaded_organic" stroke="#82ca9d" name="Loaded Organic" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default Charts;