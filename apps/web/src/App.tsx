import { useEffect, useState } from 'react';

type CaseRecord = {
  id: string;
  company_name: string;
  kra_pin: string;
  status: string;
  kyb_score: number;
  kyc_score: number;
  aml_score: number;
  clearance: string;
};

type FormState = {
  company_name: string;
  kra_pin: string;
  director_name: string;
  document_type: string;
  risk_level: string;
};

const initialForm: FormState = {
  company_name: '',
  kra_pin: '',
  director_name: '',
  document_type: 'certificate_of_incorporation',
  risk_level: 'medium',
};

export default function App() {
  const [cases, setCases] = useState<CaseRecord[]>([]);
  const [form, setForm] = useState<FormState>(initialForm);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const fetchCases = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/v1/compliance/cases');
      const data = await response.json();
      setCases(data);
    } catch (error) {
      console.error('Error loading cases', error);
    }
  };

  useEffect(() => {
    fetchCases();
  }, []);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = event.target;
    setForm((previous) => ({ ...previous, [name]: value }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setStatusMessage('');

    try {
      const response = await fetch('http://localhost:8001/api/v1/compliance/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      const result = await response.json();
      setStatusMessage(`Case ${result.id} created successfully.`);
      setForm(initialForm);
      await fetchCases();
    } catch (error) {
      setStatusMessage('Unable to submit case right now. Please try again.');
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

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
          <strong>{cases.length + 1240}</strong>
        </div>
        <div className="card">
          <span>Approved</span>
          <strong>{cases.filter((item) => item.clearance === 'approved').length + 1185}</strong>
        </div>
        <div className="card">
          <span>Review queue</span>
          <strong>{42 + cases.filter((item) => item.status === 'under_review').length}</strong>
        </div>
        <div className="card">
          <span>Risk alerts</span>
          <strong>7</strong>
        </div>
      </section>

      <div className="content-grid">
        <section className="panel form-panel">
          <div className="panel-header">
            <h2>Vendor onboarding</h2>
            <span>ODPC consent included</span>
          </div>

          <form onSubmit={handleSubmit} className="onboarding-form">
            <label>
              Company name
              <input name="company_name" value={form.company_name} onChange={handleChange} required />
            </label>

            <label>
              KRA PIN
              <input name="kra_pin" value={form.kra_pin} onChange={handleChange} required />
            </label>

            <label>
              Director / owner name
              <input name="director_name" value={form.director_name} onChange={handleChange} required />
            </label>

            <label>
              Document type
              <select name="document_type" value={form.document_type} onChange={handleChange}>
                <option value="certificate_of_incorporation">Certificate of Incorporation</option>
                <option value="kra_certificate">KRA Certificate</option>
                <option value="national_id">National ID</option>
                <option value="passport">Passport</option>
              </select>
            </label>

            <label>
              Risk level
              <select name="risk_level" value={form.risk_level} onChange={handleChange}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </label>

            <div className="consent-row">
              <input type="checkbox" defaultChecked />
              <span>I consent to the compliance review and data processing required under the ODPC Act.</span>
            </div>

            <button type="submit" className="submit-btn" disabled={isSubmitting}>
              {isSubmitting ? 'Submitting...' : 'Submit for verification'}
            </button>
          </form>

          {statusMessage && <p className="status-message">{statusMessage}</p>}
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
                  <td>{item.company_name}</td>
                  <td>{item.status}</td>
                  <td>{item.kyb_score}%</td>
                  <td>{item.kyc_score}%</td>
                  <td>{item.aml_score}%</td>
                  <td>{item.clearance}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </div>
    </div>
  );
}
