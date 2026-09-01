import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const { logout } = useAuth();

  return (
    <div>
      <h1>DocuMind Dashboard</h1>

      <p>You are authenticated.</p>

      <button onClick={logout}>
        Logout
      </button>
    </div>
  );
}

export default Dashboard;