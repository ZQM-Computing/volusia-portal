const fs = require('fs');
const path = require('path');

const fpath = path.join(process.cwd(), 'src/pages/HomePage.tsx');
let data = fs.readFileSync(fpath, 'utf-8');

const footer = `

    {/* Metadata Footer */}
    <footer className="bg-gray-50 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h3 className="text-lg font-bold text-volusia-navy mb-4">Data Sources & Metadata</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Population</h4>
            {population && <p className="text-volusia-slate mb-1">Current: {population.toLocaleString()} residents</p>}
            {medianAge && <p className="text-volusia-slate mb-1">Median Age: {medianAge}</p>}
            {pctBachelor !== undefined && <p className="text-volusia-slate mb-1">Bachelor+: {pctBachelor}%</p>}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Income</h4>
            {medianHouseholdIncome && <p className="text-volusia-slate mb-1">Median HH Income: ${'$'}{medianHouseholdIncome.toLocaleString()}</p>}
            {personalIncome && <p className="text-volusia-slate mb-1">Per Capita: ${'$'}{personalIncome.toLocaleString()}</p>}
            {unemploymentACS !== undefined && <p className="text-volusia-slate mb-1">Unemployment: {unemploymentACS}%</p>}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Climate</h4>
            {temp && <p className="text-volusia-slate mb-1">Avg Temp: {temp}°F</p>}
            {precipitation && <p className="text-volusia-slate mb-1">Rainfall: {precipitation}"</p>}
            {costOfLivingIdx !== undefined && <p className="text-volusia-slate mb-1">Cost of Living Index: {costOfLivingIdx}</p>}
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-gray-200 text-xs text-gray-400">
          <p>Project Volusia Data Portal — All data sourced from public APIs (Census ACS, BLS QCEW, NOAA NCEI, C2ER). Last updated: {new Date().toLocaleString()}</p>
        </div>
      </div>
    </footer>`;

// Find the closing block and insert the footer BEFORE it
// The closing block is: '    </div>\n  )\n}\n'
// The footer should be inserted BEFORE the closing div
// So the new closing is: '    </div>' + footer + '\n  )\n}\n'
const oldClosing = '    </div>\n  )\n}\n';
const newClosing = '    </div>' + footer + '\n  )\n}\n';

if (!data.includes(oldClosing)) {
    console.error('Closing block not found');
    process.exit(1);
}

data = data.replace(oldClosing, newClosing);
fs.writeFileSync(fpath, data);
console.log('OK');