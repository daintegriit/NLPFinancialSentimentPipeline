import React from "react";

const ExtremeScoresTable = ({ data }) => {
  console.log("📩 Incoming data to ExtremeScoresTable:", data);

  if (!data || data.length === 0)
    return <p className="text-yellow-300">⚠️ No sentiment data loaded.</p>;

  // ✅ Log everything once for debug
  console.log("🔍 Full row dump:", data.map(row => ({
    fin: row.score_finbert,
    rob: row.score_roberta,
    title: row.title
  })));

  // ✅ Proper filter
  const extremes = data.filter((row) => {
    const fin = Number(row?.score_finbert);
    const rob = Number(row?.score_roberta);

    const finExtreme = !isNaN(fin) && (fin >= 0.95 || fin <= 0.05);
    const robExtreme = !isNaN(rob) && (rob >= 0.95 || rob <= 0.05);

    if (finExtreme || robExtreme) {
      console.log("🚨 EXTREME DETECTED:", { title: row.title, fin, rob });
    }

    return finExtreme || robExtreme;
  });



  console.log("✅ Filtered extremes:", extremes);

  if (extremes.length === 0) {
    return (
      <p className="text-green-400">
        ✅ No extreme sentiment headlines detected.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <h2 className="text-xl font-bold text-red-400 mb-2">
        🚨 Extremely High or Low Sentiment
      </h2>
      <table className="min-w-full bg-gray-900 text-white border border-gray-700 rounded">
        <thead>
          <tr className="bg-gray-800 text-sm">
            <th className="px-4 py-2 border">Title</th>
            <th className="px-4 py-2 border">FinBERT Score</th>
            <th className="px-4 py-2 border">RoBERTa Score</th>
            <th className="px-4 py-2 border">Published</th>
            <th className="px-4 py-2 border">Link</th>
          </tr>
        </thead>
        <tbody>
          {extremes.map((row, idx) => (
            <tr key={idx} className="hover:bg-gray-800">
              <td className="px-4 py-2 border">{row.title}</td>
              <td className="px-4 py-2 border">
                {parseFloat(row.score_finbert).toFixed(2)}
              </td>
              <td className="px-4 py-2 border">
                {parseFloat(row.score_roberta).toFixed(2)}
              </td>
              <td className="px-4 py-2 border">{row.published}</td>
              <td className="px-4 py-2 border">
                <a
                  href={row.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 underline"
                >
                  Open
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ExtremeScoresTable;
