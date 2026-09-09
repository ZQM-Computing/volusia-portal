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

const pages = ['HomePage.tsx', 'TouristsPage.tsx', 'BusinessPage.tsx', 'LeadersPage.tsx', 'ResidentsPage.tsx'];

pages.forEach(page => {
    const fpath = path.join(process.cwd(), 'src/pages', page);
    let data = fs.readFileSync(fpath, 'utf-8');

    if (data.includes('{/* Metadata Footer */}')) {
        console.log('SKIP ' + page + ' (already has footer)');
        return;
    }

    // Try multiple closing block patterns
    const patterns = [
        '    </div>\n  )\n}\n',
        '    </div>\r\n  )\r\n}\r\n',
        'Card>\n      </div>\n    </div>\n  )\n}\n',
        'Card>\r\n      </div>\r\n    </div>\r\n  )\r\n}\r\n',
        '</button>\n        </Card>\n      </div>\n    </div>\n  )\n}\n',
        '</button>\r\n        </Card>\r\n      </div>\r\n    </div>\r\n  )\r\n}\r\n',
        'd>\n      </div>\n    </div>\n  )\n}\n',
        'd>\r\n      </div>\r\n    </div>\r\n  )\r\n}\r\n',
    ];

    let replaced = false;
    for (const oldStr of patterns) {
        if (data.includes(oldStr)) {
            const newStr = '    </div>' + footer_jsx + '\n  )\n}\n';
            data = data.replace(oldStr, newStr);
            fs.writeFileSync(fpath, data);
            console.log('OK ' + page + ' (pattern: ' + JSON.stringify(oldStr.substring(0, 30)) + '...)');
            replaced = true;
            break;
        }
    }

    if (!replaced) {
        console.error('FAIL ' + page + ' - no closing pattern found');
        // Show last 10 lines
        const lines = data.split(/\r?\n/);
        console.error('Last 10 lines:');
        lines.slice(-10).forEach((l, i) => console.error('  ' + (lines.length - 10 + i + 1) + ': ' + l));
    }
});