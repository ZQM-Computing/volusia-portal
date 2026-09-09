const fs = require('fs');
const path = require('path');

const base = process.cwd();

// Footer JSX - same structure as LeadersPage (working)
const footer_jsx = `
    {/* Metadata Footer */}
    <footer className="bg-gray-50 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h3 className="text-lg font-bold text-volusia-navy mb-4">Data Sources & Metadata</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Economic Indicators</h4>
            {economic?.indicators?.slice(0, 3).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-400">Source: {i.source} | Vintage: {i.vintage} | Fetched: {new Date(i.fetched_at).toLocaleString()}</span>
              </div>
            ))}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Demographics</h4>
            {(economic?.indicators || []).slice(0, 0).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-400">Source: {i.source} | Vintage: {i.vintage}</span>
              </div>
            ))}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Climate</h4>
            {(economic?.indicators || []).slice(0, 0).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-400">Source: {i.source} | Vintage: {i.vintage}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-gray-200 text-xs text-gray-400">
          <p>Project Volusia Data Portal — All data sourced from public APIs (Census ACS, BLS QCEW, NOAA NCEI, C2ER). Last updated: {new Date().toLocaleString()}</p>
        </div>
      </div>
    </footer>`;

const fname = path.join(base, 'src/pages', process.argv[2]);
let data = fs.readFileSync(fname, 'utf-8');

if (data.includes('{/* Metadata Footer */}')) {
    console.log('Already has footer, skipping');
    process.exit(0);
}

// BusinessPage uses CRLF line endings - 'Card>\r\n        </Card>\r\n      </div>\r\n    </div>\r\n  )\r\n}\r\n'
const oldClosing = process.argv[3] || '    </div>\n  )\n}\n';
const newClosing = '    </div>' + footer_jsx + '\n  )\n}\n';

if (!data.includes(oldClosing)) {
    console.error('Closing block not found in ' + process.argv[2]);
    console.error('Looking for: ' + JSON.stringify(oldClosing));
    console.error('Actual bytes around end:');
    const idx = data.lastIndexOf('  )\r\n}\r\n');
    console.error(JSON.stringify(data.substring(idx-50, idx+20)));
    process.exit(1);
}

data = data.replace(oldClosing, newClosing);
fs.writeFileSync(fname, data);
console.log('OK ' + process.argv[2]);