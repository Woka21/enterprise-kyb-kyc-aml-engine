const cases = [
  {
    id: 'case-1001',
    company: 'Nairobi Traders Ltd',
    status: 'Under review',
    kyb: 92,
    kyc: 88,
    aml: 96,
    clearance: 'Pending',
  },
  {
    id: 'case-1002',
    company: 'Kenya Capital Group',
    status: 'Cleared',
    kyb: 97,
    kyc: 94,
    aml: 99,
    clearance: 'Approved',
  },
];

export default function App() {
  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Enterprise compliance platform</p>
          <h1>KYB / KYC / AML Engine</h1>
        </div>
        <button className="primary-btn">New compliance check</button>
      </header>

      <section className="summary-cards">
        <div className="card">
          <span>Total checks</span>
          <strong>1,284</strong>
        </div>
        <div className="card">
          <span>Approved</span>
          <strong>1,185</strong>
        </div>
        <div className="card">
          <span>Review queue</span>
          <strong>42</strong>
        </div>
        <div className="card">
          <span>Risk alerts</span>
          <strong>7</strong>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Executive review dashboard</h2>
          <span>Last synced 2m ago</span>
        </div>

        <table>
          <thead>
            <tr>
              <th>Client</th>
              <th>Status</th>
              <th>KYB</th>
              <th>KYC</th>
              <th>AML</th>
              <th>Clearance</th>
            </tr>
          </thead>
          <tbody>
            {cases.map((item) => (
              <tr key={item.id}>
                <td>{item.company}</td>
                <td>{item.status}</td>
                <td>{item.kyb}%</td>
                <td>{item.kyc}%</td>
                <td>{item.aml}%</td>
                <td>{item.clearance}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
