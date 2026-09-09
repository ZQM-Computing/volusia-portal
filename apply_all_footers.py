"""Add metadata footer to all 5 pages - insert before the closing of the main component return."""
import os

base = r'C:\Users\zqmco\Docker\volusia-portal'

footer_jsx = """
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
            {medianHouseholdIncome && <p className="text-volusia-slate mb-1">Median HH Income: ${medianHouseholdIncome.toLocaleString()}</p>}
            {personalIncome && <p className="text-volusia-slate mb-1">Per Capita: ${personalIncome.toLocaleString()}</p>}
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
    </footer>"""

def add_footer(fname):
    fpath = os.path.join(base, fname)
    with open(fpath, 'rb') as fh:
        data = fh.read().decode('utf-8').replace('\r\n', '\n')
    
    # For HomePage: the return statement ends with '    </div>\n  )\n}'
    # The footer should be inserted before the closing div
    # Find the last occurrence of the closing pattern
    old = "    </div>\n  )\n}"
    if old in data:
        new = "    </div>" + footer_jsx + "\n  )\n}"
        data = data.replace(old, new, 1)
        with open(fpath, 'wb') as fh:
            fh.write(data.encode('utf-8'))
        print(f"OK {fname}")
        return
    
    # For other pages: the closing might be different
    # Try to find the component closing
    idx = data.rfind('}\n')
    if idx >= 0:
        # Insert footer before the closing
        new = footer_jsx + "\n}\n"
        data = data[:idx] + new
        with open(fpath, 'wb') as fh:
            fh.write(data.encode('utf-8'))
        print(f"OK {fname}")
        return
    
    print(f"FAILED {fname}: could not find closing block")

for f in ['src/pages/HomePage.tsx', 'src/pages/TouristsPage.tsx', 'src/pages/BusinessPage.tsx']:
    add_footer(f)