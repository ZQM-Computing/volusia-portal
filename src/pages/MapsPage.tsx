import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, GeoJSON, CircleMarker, Popup } from 'react-leaflet'
import { useMapLayers } from '../hooks/useApi'
import { Card, SectionTitle, Badge } from '../components/UI'

export function MapsPage() {
  const { data: mapLayers, loading } = useMapLayers()
  const [activeCategory, setActiveCategory] = useState<string>('all')
  const [showBoundary, setShowBoundary] = useState(true)
  const [showCities, setShowCities] = useState(false)

  const layers = mapLayers ?? []
  const filteredLayers = activeCategory === 'all'
    ? layers
    : layers.filter((l: any) => l.category === activeCategory)

  // Collect all GeoJSON features from map layers that have geometry
  const geojsonFeatures = filteredLayers
    .filter((l: any) => l.geometry)
    .map((l: any) => {
      try {
        const geojson = JSON.parse(l.geometry)
        return geojson
      } catch {
        return null
      }
    })
    .filter(Boolean)

  // Merge features into a single FeatureCollection for rendering
  const mergedGeoJSON = geojsonFeatures.length > 0
    ? { type: 'FeatureCollection' as const, features: geojsonFeatures as any[] }
    : null

  const categories = ['all', 'boundary', 'economic', 'infrastructure', 'environment', 'demographic', 'cultural']

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Interactive Maps"
        subtitle={`Explore Volusia County through ${layers.length} geographic data layers`}
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
                  {cat === 'all' ? 'All Layers' : cat.charAt(0).toUpperCase() + cat.slice(1)}
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
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">
              Layers{loading ? '…' : ` (${filteredLayers.length})`}
            </h3>
            <div className="space-y-2">
              {loading ? (
                <div className="text-xs text-volusia-slate animate-pulse">Loading layers…</div>
              ) : filteredLayers.length === 0 ? (
                <div className="text-xs text-volusia-slate">No layers in this category.</div>
              ) : (
                filteredLayers.map((layer: any) => (
                  <div key={layer.id} className="text-xs p-2 bg-gray-50 rounded">
                    <div className="font-medium text-volusia-navy">{layer.name}</div>
                    <div className="text-gray-500 mt-0.5">{layer.source}</div>
                  </div>
                ))
              )}
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
              {showBoundary && mergedGeoJSON && (
                <GeoJSON
                  data={mergedGeoJSON}
                  style={{
                    color: '#0d7377',
                    weight: 2,
                    fillColor: '#0d7377',
                    fillOpacity: 0.15,
                  }}
                />
              )}
              {showCities && layers.filter((l: any) => l.geometry && l.type === 'Point').map((layer: any) => {
                try {
                  const geojson = JSON.parse(layer.geometry)
                  if (geojson.type === 'FeatureCollection') {
                    return geojson.features.map((feat: any, i: number) => (
                      <CircleMarker
                        key={`${layer.id}-${i}`}
                        center={[feat.geometry.coordinates[1], feat.geometry.coordinates[0]]}
                        radius={5}
                        pathOptions={{ color: '#c9a84c', fillColor: '#c9a84c', fillOpacity: 0.8, weight: 2 }}
                      >
                        <Popup>
                          <div className="text-sm">
                            <strong>{layer.name}</strong>
                            <br />
                            {feat.properties?.name && <div>{feat.properties.name}</div>}
                          </div>
                        </Popup>
                      </CircleMarker>
                    ))
                  }
                } catch { return null }
                return null
              })}
            </MapContainer>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Map data: OpenStreetMap contributors. {layers.length} layers registered via /map-layers.json.
            {loading ? ' Loading…' : `${filteredLayers.length} layers shown`}.
          </p>
        </div>
      </div>
    </div>
  )
}
