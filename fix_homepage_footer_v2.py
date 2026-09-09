"""Add metadata footer to HomePage.tsx — correct structure."""
import os

base = r'C:\Users\zqmco\Docker\volusia-portal'

# Footer JSX - properly structured with all tags balanced
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

fpath = os.path.join(base, 'src/pages/HomePage.tsx')
with open(fpath, 'rb') as fh:
    data = fh.read().decode('utf-8').replace('\r\n', '\n')

# HomePage closing: '    </div>\n  )\n}\n' (no blank line after })
old = "    </div>\n  )\n}\n"
assert old in data, f"HomePage: closing block not found"
new = "    </div>" + footer_jsx + "\n  )\n}\n"
data = data.replace(old, new, 1)
with open(fpath, 'wb') as fh:
    fh.write(data.encode('utf-8'))
print(f"OK {fpath}")