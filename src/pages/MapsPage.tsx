import { useState } from 'react'
import { MapContainer, TileLayer, GeoJSON, CircleMarker, Popup } from 'react-leaflet'
import { mapLayers } from '../data/sampleData'
import { Card, SectionTitle, Badge } from '../components/UI'

// Simplified Volusia County boundary polygon (approximate)
const volusiaBoundary = {
  type: 'Feature' as const,
  properties: { name: 'Volusia County' },
  geometry: {
    type: 'MultiPolygon' as const,
    coordinates: [
      [
        [
          [-81.5, 29.4], [-80.8, 29.4], [-80.8, 28.6], [-81.0, 28.6],
          [-81.1, 28.8], [-81.4, 28.9], [-81.5, 29.1], [-81.5, 29.4],
        ],
      ],
    ],
  },
}

// Sample city markers for Volusia County
const cityMarkers = [
  { name: 'Daytona Beach', coords: [29.2108, -81.0228], pop: 72000 },
  { name: 'DeLand', coords: [29.0283, -81.3031], pop: 41000 },
  { name: 'New Smyrna Beach', coords: [29.0258, -80.927], pop: 28000 },
  { name: 'Ormond Beach', coords: [29.2858, -81.0559], pop: 44000 },
  { name: 'Port Orange', coords: [29.1383, -80.9956], pop: 65000 },
  { name: 'Deltona', coords: [28.9005, -81.2637], pop: 93000 },
]

export function MapsPage() {
  const [activeCategory, setActiveCategory] = useState<string>('boundary')
  const [showBoundary, setShowBoundary] = useState(true)
  const [showCities, setShowCities] = useState(true)

  const categories = ['boundary', 'economic', 'infrastructure', 'environment', 'demographic', 'cultural']
  const filteredLayers = mapLayers.filter((l) => l.category === activeCategory)

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Interactive Maps"
        subtitle="Explore Volusia County through geographic data layers"
      />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1 space-y-4">
          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">Layer Category</h3>
            <div className="space-y-1">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={`w-full text-left px-3 py-2 rounded text-sm transition-colors ${
                    activeCategory === cat
                      ? 'bg-volusia-teal text-white'
                      : 'text-volusia-slate hover:bg-gray-100'
                  }`}
                >
                  {cat.charAt(0).toUpperCase() + cat.slice(1)}
                </button>
              ))}
            </div>
          </Card>

          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">Quick Toggles</h3>
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-sm text-volusia-slate cursor-pointer">
                <input
                  type="checkbox"
                  checked={showBoundary}
                  onChange={(e) => setShowBoundary(e.target.checked)}
                  className="rounded text-volusia-teal"
                />
                County Boundary
              </label>
              <label className="flex items-center gap-2 text-sm text-volusia-slate cursor-pointer">
                <input
                  type="checkbox"
                  checked={showCities}
                  onChange={(e) => setShowCities(e.target.checked)}
                  className="rounded text-volusia-teal"
                />
                City Markers
              </label>
            </div>
          </Card>

          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">Layers in Category</h3>
            <div className="space-y-2">
              {filteredLayers.map((layer) => (
                <div key={layer.id} className="text-xs p-2 bg-gray-50 rounded">
                  <div className="font-medium text-volusia-navy">{layer.name}</div>
                  <div className="text-gray-500 mt-0.5">{layer.source}</div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Map */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100" style={{ height: '600px' }}>
            <MapContainer
              center={[29.1, -81.05]}
              zoom={9}
              style={{ height: '100%', width: '100%' }}
              scrollWheelZoom={true}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              {showBoundary && (
                <GeoJSON
                  data={volusiaBoundary as any}
                  style={{
                    color: '#0d7377',
                    weight: 3,
                    fillColor: '#0d7377',
                    fillOpacity: 0.05,
                  }}
                />
              )}
              {showCities &&
                cityMarkers.map((city) => (
                  <CircleMarker
                    key={city.name}
                    center={[city.coords[0], city.coords[1]]}
                    radius={Math.sqrt(city.pop) / 10}
                    pathOptions={{
                      color: '#c9a84c',
                      fillColor: '#c9a84c',
                      fillOpacity: 0.6,
                      weight: 2,
                    }}
                  >
                    <Popup>
                      <div className="text-sm">
                        <strong>{city.name}</strong>
                        <br />
                        Pop: {city.pop.toLocaleString()}
                      </div>
                    </Popup>
                  </CircleMarker>
                ))}
            </MapContainer>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Map data: OpenStreetMap contributors. County boundary: US Census TIGER/Line (simplified for demo).
            Full GeoJSON layers available via API.
          </p>
        </div>
      </div>
    </div>
  )
}
