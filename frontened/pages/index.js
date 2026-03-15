import MatchTable from '../components/MatchTable';
import { useEffect, useState } from 'react';

export default function Home() {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/matches')
      .then(res => res.json())
      .then(data => setMatches(data));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Football Betting Dashboard</h1>
      <MatchTable matches={matches} />
    </div>
  );
}
