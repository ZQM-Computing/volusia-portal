const fs = require('fs');
const path = require('path');

const leadersPath = path.join(process.cwd(), 'src/pages/LeadersPage.tsx');
let data = fs.readFileSync(leadersPath, 'utf-8');

const marker = '{/* Metadata Footer */}';
const count = (data.match(new RegExp(marker.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
console.log('Current footers: ' + count);

if (count > 1) {
    // Remove all footers (inside map callbacks)
    let idx = data.indexOf(marker);
    while (idx >= 0) {
        const footerStart = data.lastIndexOf('\n    <footer', idx);
        if (footerStart >= 0) {
            const footerEnd = data.indexOf('</footer>', footerStart) + '</footer>'.length;
            data = data.substring(0, footerStart) + data.substring(footerEnd);
        }
        idx = data.indexOf(marker);
    }
    console.log('Removed all footers');

    // Add one footer before the closing block
    const closingPattern = '            </div>\n        </div>\n    )\n}\n';
    const insertPoint = data.lastIndexOf(closingPattern);
    if (insertPoint >= 0) {
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
        data = data.substring(0, insertPoint) + footer_jsx + '\n' + data.substring(insertPoint);
        fs.writeFileSync(leadersPath, data);
        console.log('OK - added 1 footer to LeadersPage.tsx');
    } else {
        console.error('FAIL - closing pattern not found');
    }
} else {
    console.log('LeadersPage.tsx already correct');
}