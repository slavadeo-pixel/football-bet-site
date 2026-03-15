export default function MatchTable({ matches }) {
  return (
    <table className="min-w-full border border-gray-300">
      <thead>
        <tr>
          <th className="border p-2">League</th>
          <th className="border p-2">Home</th>
          <th className="border p-2">Away</th>
          <th className="border p-2">Home Value</th>
          <th className="border p-2">Draw Value</th>
          <th className="border p-2">Away Value</th>
          <th className="border p-2">Recommendations</th>
        </tr>
      </thead>
      <tbody>
        {matches.map((m, i) => (
          <tr key={i}>
            <td className="border p-2">{m.league}</td>
            <td className="border p-2">{m.home_team}</td>
            <td className="border p-2">{m.away_team}</td>
            <td className={`border p-2 ${m.highlight.home === 'green' ? 'bg-green-300' : m.highlight.home === 'yellow' ? 'bg-yellow-300' : 'bg-red-300'}`}>{m.value.home}%</td>
            <td className={`border p-2 ${m.highlight.draw === 'green' ? 'bg-green-300' : m.highlight.draw === 'yellow' ? 'bg-yellow-300' : 'bg-red-300'}`}>{m.value.draw}%</td>
            <td className={`border p-2 ${m.highlight.away === 'green' ? 'bg-green-300' : m.highlight.away === 'yellow' ? 'bg-yellow-300' : 'bg-red-300'}`}>{m.value.away}%</td>
            <td className="border p-2">{m.recommendations.join(", ")}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
