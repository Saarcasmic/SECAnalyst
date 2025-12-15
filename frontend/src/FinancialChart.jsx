import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const FinancialChart = ({ data }) => {
    // Transform backend data format to Recharts format
    // Backend: { labels: ['2022', '2023'], datasets: [{ name: 'AAPL', data: [100, 200] }] }
    // Recharts: [{ name: '2022', AAPL: 100 }, { name: '2023', AAPL: 200 }]

    const chartData = data.labels.map((label, index) => {
        const point = { name: label };
        data.datasets.forEach(dataset => {
            point[dataset.name] = dataset.data[index];
        });
        return point;
    });

    const colors = ['#2563eb', '#16a34a', '#dc2626', '#d97706']; // Blue, Green, Red, Amber

    return (
        <div className="w-full h-64 bg-white p-4 rounded-xl border border-gray-100 shadow-sm mt-2">
            <h3 className="text-sm font-semibold text-gray-700 mb-4 text-center">{data.title}</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart
                    data={chartData}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                    <XAxis dataKey="name" tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
                    <YAxis
                        tick={{ fontSize: 12 }}
                        axisLine={false}
                        tickLine={false}
                        tickFormatter={(value) => `$${(value / 1e9).toFixed(0)}B`}
                    />
                    <Tooltip
                        cursor={{ fill: '#f3f4f6' }}
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        formatter={(value) => [`$${(value / 1e9).toFixed(2)}B`, undefined]}
                    />
                    <Legend />
                    {data.datasets.map((dataset, index) => (
                        <Bar
                            key={dataset.name}
                            dataKey={dataset.name}
                            fill={colors[index % colors.length]}
                            radius={[4, 4, 0, 0]}
                        />
                    ))}
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default FinancialChart;
