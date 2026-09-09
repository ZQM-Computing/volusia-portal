const fs = require('fs');
const path = require('path');

const footer_jsx = `
    {/* Metadata Footer */}
    <footer className="bg-gray-50 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h3 className="text-lg font-bold text-volusia-navy mb-4">Data Sources & Metadata</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Economic Indicators</h4>
            {(economic?.indicators || []).slice(0, 3).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-400">Source: {i.source} | Vintage: {i.vintage} | Fetched: {new Date(i.fetched_at).toLocaleString()}</span>
              </div>
            ))}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Demographics</h4>
            {(economic?.indicators || []).slice(3, 6).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-400">Source: {i.source} | Vintage: {i.vintage}</span>
              </div>
            ))}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Climate</h4>
            {(economic?.indicators || []).slice(6, 9).map((i: any) => (
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

const pages = [
    { name: 'HomePage.tsx', closing: '    </div>\n  )\n}\n' },
    { name: 'BusinessPage.tsx', closing: '        </Card>\n      </div>\n    </div>\n  )\n}\n' },
    { name: 'TouristsPage.tsx', closing: '        </Card>\n      </div>\n    </div>\n  )\n}\n' },
    { name: 'LeadersPage.tsx', closing: '            </div>\n        </div>\n    )\n}\n' },
    { name: 'ResidentsPage.tsx', closing: '      </div>\n    </div>\n  )\n}\n' },
];

pages.forEach(({ name, closing }) => {
    const fpath = path.join(process.cwd(), 'src/pages', name);
    let data = fs.readFileSync(fpath, 'utf-8');

    // Remove existing footer if present
    const marker = '{/* Metadata Footer */}';
    if (data.includes(marker)) {
        const idx = data.indexOf(marker);
        const footerStart = data.lastIndexOf('\n    <footer', idx);
        if (footerStart >= 0) {
            const footerEnd = data.indexOf('</footer>', footerStart) + '</footer>'.length;
            data = data.substring(0, footerStart) + data.substring(footerEnd);
            console.log('REMOVED existing footer from ' + name);
        }
    }

    // Insert footer before the closing block
    if (data.includes(closing)) {
        const insertPoint = data.indexOf(closing);
        const before = data.substring(0, insertPoint);
        const after = data.substring(insertPoint);
        data = before + footer_jsx + '\n' + after;
        fs.writeFileSync(fpath, data);
        console.log('OK ' + name);
    } else {
        console.error('FAIL ' + name + ' - closing pattern not found');
        // Show last 20 lines for debugging
        const lines = data.split('\n');
        console.log('Last 10 lines:');
        lines.slice(-10).forEach((l, i) => console.log(`  ${lines.length - 10 + i + 1}: ${repr(l)}`));
    }
});