import { useEffect, useState } from "react";
import api from "./services/api";

function App() {
  const [message, setMessage] = useState("Checking API...");

  useEffect(() => {
    const checkApi = async () => {
      try {
        const response = await api.get("/api/health");

        setMessage(response.data.message);
      } catch (error) {
        console.error(error);
        setMessage("Unable to connect to API");
      }
    };

    checkApi();
  }, []);

  return (
    <div>
      <h1>DocuMind</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;