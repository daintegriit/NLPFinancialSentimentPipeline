// frontend/src/components/HeadlinesTable.jsx
import React from "react";

const HeadlinesTable = ({ data }) => {
  if (!data || data.length === 0) {
    return <p className="text-green-400">✅ No headlines found.</p>;
  }

  // Sort by published date (most recent first)
  const sortedData = [...data].sort(
    (a, b) => new Date(b.published) - new Date(a.published)
  );

  return (
    <div className="overflow-x-auto">
      <h2 className="text-xl font-bold text-blue-300 mb-2">
        📰 News Headlines and Sentiment
      </h2>
      <table className="min-w-full bg-gray-900 text-white border border-gray-700 rounded">
        <thead>
          <tr className="bg-gray-800 text-sm">
            <th className="px-4 py-2 border">Title</th>
            <th className="px-4 py-2 border">Sentiment</th>
            <th className="px-4 py-2 border">FinBERT Score</th>
            <th className="px-4 py-2 border">RoBERTa Score</th>
            <th className="px-4 py-2 border">Published</th>
            <th className="px-4 py-2 border">Link</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, idx) => (
            <tr key={idx} className="hover:bg-gray-800">
              <td className="px-4 py-2 border">{row.title}</td>
              <td className="px-4 py-2 border">{row.label_finbert}</td>
              <td className="px-4 py-2 border">
                {row.score_finbert != null
                  ? parseFloat(row.score_finbert).toFixed(2)
                  : "N/A"}
              </td>
              <td className="px-4 py-2 border">
                {row.score_roberta != null
                  ? parseFloat(row.score_roberta).toFixed(2)
                  : "N/A"}
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

export default HeadlinesTable;
