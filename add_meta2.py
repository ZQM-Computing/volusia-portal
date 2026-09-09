"""Add metadata footers to LeadersPage, ResidentsPage, TouristsPage."""
import os

base = r'C:\Users\zqmco\Docker\volusia-portal'
footer_html = """
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
            {climateIndicators?.slice(0, 3).map((i: any) => (
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
    </footer>
"""

pages = {
    'src/pages/LeadersPage.tsx': ('            {/* Data Room CTA */}', footer_html + '\n            {/* Data Room CTA */}'),
    'src/pages/ResidentsPage.tsx': ('      {/* Resources */}', footer_html + '\n      {/* Resources */}'),
    'src/pages/TouristsPage.tsx': ('        </section>\n      )}', '        </section>\n      )}\n\n' + footer_html + '\n    </div>'),
}

for rel_path, (old, new) in pages.items():
    path = os.path.join(base, rel_path)
    with open(path, 'rb') as f:
        data = f.read()
    text = data.decode('utf-8').replace('\r\n', '\n')
    
    if old not in text:
        print(f"SKIP {rel_path}: old string not found")
        print(f"  Looking for: {repr(old[:80])}")
        continue
    
    text = text.replace(old, new, 1)
    
    with open(path, 'wb') as f:
        f.write(text.encode('utf-8'))
    print(f"OK {rel_path}")

print("Done")