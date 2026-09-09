import re

# Fix LeadersPage.tsx - remove ALL footers, add exactly one at correct position
with open('src/pages/LeadersPage.tsx', 'r') as f:
    data = f.read()

marker = '{/* Metadata Footer */}'
count = data.count(marker)
print('Current footers:', count)

# Remove ALL footers - use a more robust approach
# Each footer starts with '{/* Metadata Footer */}' followed by <footer>...</footer>
# Remove from marker to </footer>
while marker in data:
    idx = data.find(marker)
    footer_end = data.find('</footer>', idx) + len('</footer>')
    data = data[:idx] + data[footer_end:]
    print('Removed one footer')

print('After removal, footers:', data.count(marker))

# Find the correct closing position - before the component's final closing block
# LeadersPage structure: the component closes with:
#             </div>
#         </div>
#     )
# }
closing = '            </div>\n        </div>\n    )\n}\n'
insert_point = data.rfind(closing)
print('Insert point:', insert_point)

if insert_point >= 0:
    footer_jsx = '''
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
    </footer>'''
    data = data[:insert_point] + footer_jsx + '\n' + data[insert_point:]
    with open('src/pages/LeadersPage.tsx', 'w') as f:
        f.write(data)
    print('OK - fixed LeadersPage.tsx, 1 footer')
else:
    print('FAIL - closing pattern not found')