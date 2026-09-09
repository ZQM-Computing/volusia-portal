"""Add metadata footers — precise fix using correct closing depth."""
import os

base = r'C:\Users\zqmco\Docker\volusia-portal'

# The footer JSX - indented at the same level as the page content
footer = """

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
            {demographics?.indicators?.slice(0, 3).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-400">Source: {i.source} | Vintage: {i.vintage} | Fetched: {new Date(i.fetched_at).toLocaleString()}</span>
              </div>
            ))}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Climate</h4>
            {climate?.slice(0, 3).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-400">Source: {i.source} | Vintage: {i.vintage} | Fetched: {new Date(i.fetched_at).toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-gray-200 text-xs text-gray-400">
          <p>Project Volusia Data Portal — All data sourced from public APIs (Census ACS, BLS QCEW, NOAA NCEI, C2ER). Last updated: {new Date().toLocaleString()}</p>
        </div>
      </div>
    </footer>"""

# BusinessPage - the closing is `      </div>\n    </div>\n  )\n}`
# That's 2 closing divs (the page content wrapper + the main container)
# Then `)` for the component return, then `}` for the component
f = os.path.join(base, 'src/pages/BusinessPage.tsx')
with open(f, 'rb') as fh:
    data = fh.read().decode('utf-8').replace('\r\n', '\n')

# Find the exact closing pattern
old = "      </div>\n    </div>\n  )\n}"
assert old in data, f"BusinessPage: old string not found"
new = "      </div>\n    </div>" + footer + "\n  )\n}"
data = data.replace(old, new, 1)
with open(f, 'wb') as fh:
    fh.write(data.encode('utf-8'))
print(f"OK {f}")

# TouristsPage - same closing pattern
f = os.path.join(base, 'src/pages/TouristsPage.tsx')
with open(f, 'rb') as fh:
    data = fh.read().decode('utf-8').replace('\r\n', '\n')
assert old in data, f"TouristsPage: old string not found"
data = data.replace(old, new, 1)
with open(f, 'wb') as fh:
    fh.write(data.encode('utf-8'))
print(f"OK {f}")

print("Done")