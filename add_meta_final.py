"""Add metadata footers to all 5 frontend pages — fixed version."""
import os

base = r'C:\Users\zqmco\Docker\volusia-portal'

# Common footer HTML for all pages
footer = """
    {/* Metadata Footer */}
    <footer className="bg-gray-50 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h3 className="text-lg font-bold text-volusia-navy mb-4">Data Sources & Metadata</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Economic Indicators</h4>
            {{economic?.indicators?.slice(0, 3).map((i: any) => (
              <div key={{i.name}} className="text-volusia-slate mb-1">
                <span className="font-medium">{{i.name}}:</span> {{i.value}} {{i.unit}}
                <br/><span className="text-xs text-gray-400">Source: {{i.source}} | Vintage: {{i.vintage}} | Fetched: {{new Date(i.fetched_at).toLocaleString()}}</span>
              </div>
            ))}}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Demographics</h4>
            {{demographics?.indicators?.slice(0, 3).map((i: any) => (
              <div key={{i.name}} className="text-volusia-slate mb-1">
                <span className="font-medium">{{i.name}}:</span> {{i.value}} {{i.unit}}
                <br/><span className="text-xs text-gray-400">Source: {{i.source}} | Vintage: {{i.vintage}} | Fetched: {{new Date(i.fetched_at).toLocaleString()}}</span>
              </div>
            ))}}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Climate</h4>
            {{climate?.slice(0, 3).map((i: any) => (
              <div key={{i.name}} className="text-volusia-slate mb-1">
                <span className="font-medium">{{i.name}}:</span> {{i.value}} {{i.unit}}
                <br/><span className="text-xs text-gray-400">Source: {{i.source}} | Vintage: {{i.vintage}} | Fetched: {{new Date(i.fetched_at).toLocaleString()}}</span>
              </div>
            ))}}
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-gray-200 text-xs text-gray-400">
          <p>Project Volusia Data Portal — All data sourced from public APIs (Census ACS, BLS QCEW, NOAA NCEI, C2ER). Last updated: {{new Date().toLocaleString()}}</p>
        </div>
      </div>
    </footer>"""

# Replace {{ with { for JSX
footer = footer.replace('{{', '{').replace('}}', '}')

# HomePage: replace {/* Mission */}
f = os.path.join(base, 'src/pages/HomePage.tsx')
with open(f, 'rb') as fh:
    data = fh.read().decode('utf-8').replace('\r\n', '\n')
old = '      {/* Mission */}'
new = footer + '\n      {/* Mission */}'
assert old in data, f"HomePage: old string not found"
data = data.replace(old, new, 1)
with open(f, 'wb') as fh:
    fh.write(data.encode('utf-8'))
print(f"OK {f}")

# LeadersPage: replace {/* Data Room CTA */}
f = os.path.join(base, 'src/pages/LeadersPage.tsx')
with open(f, 'rb') as fh:
    data = fh.read().decode('utf-8').replace('\r\n', '\n')
old = '            {/* Data Room CTA */}'
new = footer + '\n            {/* Data Room CTA */}'
assert old in data, f"LeadersPage: old string not found"
data = data.replace(old, new, 1)
with open(f, 'wb') as fh:
    fh.write(data.encode('utf-8'))
print(f"OK {f}")

# ResidentsPage: replace {/* Resources */}
f = os.path.join(base, 'src/pages/ResidentsPage.tsx')
with open(f, 'rb') as fh:
    data = fh.read().decode('utf-8').replace('\r\n', '\n')
old = '      {/* Resources */}'
new = footer + '\n      {/* Resources */}'
assert old in data, f"ResidentsPage: old string not found"
data = data.replace(old, new, 1)
with open(f, 'wb') as fh:
    fh.write(data.encode('utf-8'))
print(f"OK {f}")

# TouristsPage: replace closing block
f = os.path.join(base, 'src/pages/TouristsPage.tsx')
with open(f, 'rb') as fh:
    data = fh.read().decode('utf-8').replace('\r\n', '\n')
old = '      </div>\n    </div>\n  )\n}'
new = '      </div>\n    </div>\n\n' + footer + '\n  )\n}'
assert old in data, f"TouristsPage: old string not found"
data = data.replace(old, new, 1)
with open(f, 'wb') as fh:
    fh.write(data.encode('utf-8'))
print(f"OK {f}")

# BusinessPage: needs useClimateIndicators data as 'climate' (already destructured)
f = os.path.join(base, 'src/pages/BusinessPage.tsx')
with open(f, 'rb') as fh:
    data = fh.read().decode('utf-8').replace('\r\n', '\n')
# BusinessPage uses `climate` not `climateIndicators` - the footer uses climateIndicators
# Fix: the footer already uses `climate?.slice` for BusinessPage... wait, no.
# BusinessPage destructures: const { data: climate } = useClimateIndicators()
# So `climate` is the data array. The footer uses `climate?.slice` which is correct.
old = '      </div>\n    </div>\n  )\n}'
new = '      </div>\n    </div>\n\n' + footer + '\n  )\n}'
assert old in data, f"BusinessPage: old string not found"
data = data.replace(old, new, 1)
with open(f, 'wb') as fh:
    fh.write(data.encode('utf-8'))
print(f"OK {f}")

print("Done")